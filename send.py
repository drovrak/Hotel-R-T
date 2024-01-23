import mysql.connector
import json
def inserer_donnees_json(fichier_json):
    # Lecture des données JSON
    with open(fichier_json, 'r') as file:
        data = json.load(file)

    # Connexion à la base de données
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        database='HotelRT'
    )
    cursor = conn.cursor()

    # Insertion des données dans la table Clients
    try:
        cursor.execute('''INSERT INTO Clients (Nom, Prenom, Email, MotDePasse, Telephone) 
                          VALUES (%s, %s, %s, %s, %s)''', 
                       (data['Nom'], data['Prenom'], data['Email'], data['MotDePasse'], data['Telephone']))
        num_client = cursor.lastrowid
        type_chambre =data['Type_Chambre']
        disponible = verifier_chambre_disponible(type_chambre, data['Date_arrivee'], data['Date_depart'])
        if disponible:
        # Insertion des données dans la table Reservations
            cursor.execute('''INSERT INTO Reservations (Num_Client, Num_Chambre, Date_Arrivee, Date_Depart, Nombre_Nuits, Nombre_Personnes, Options) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                        (num_client, disponible, data['Date_arrivee'], data['Date_depart'], data['Nombre_Nuit'], data['Nombre_personnes'], json.dumps(data['Options'])))
            cursor.execute('''UPDATE Chambres SET Occupe = True, Date_Arrivee = %s, Date_Depart = %s WHERE Num_Chambre = %s''',
                        (data['Date_arrivee'],data['Date_depart'], disponible))
        else:
            print(f"La chambre de type {type_chambre} n'est pas disponible pour les dates spécifiées.")


        conn.commit()
    except mysql.connector.Error as error:
        print("Erreur lors de l'insertion des données : ", error)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("La connexion MySQL est fermée.")

def verifier_chambre_disponible(type_chambre, date_arrivee, date_depart):
    try:
        # Connexion à la base de données
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='root',
            database='HotelRT'
        )
        cursor = conn.cursor()


        # Vérifier la disponibilité de la chambre
        cursor.execute('''SELECT Num_Chambre FROM Chambres
                          WHERE Type = %s
                          AND Num_Chambre NOT IN (
                              SELECT Num_Chambre FROM Reservations
                              WHERE (Date_Arrivee BETWEEN %s AND %s) OR (Date_Depart BETWEEN %s AND %s)
                          )
                          LIMIT 1''', (type_chambre, date_arrivee, date_depart, date_arrivee, date_depart))

        result = cursor.fetchone()
        if result:
            numero_chambre = result[0]
            return numero_chambre
        else:
            return None

    except mysql.connector.Error as error:
        print("Erreur lors de la vérification de la disponibilité de la chambre : ", error)
        return False

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()