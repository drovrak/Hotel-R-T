import mysql.connector
from mysql.connector import Error


def creer_base_de_donnees():
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='root'
        )
        if conn.is_connected():
            print("Connecté avec succès à MySQL.")
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS HotelRT")
            cursor.execute("USE HotelRT")

        # Modification des tables pour inclure les nouvelles données
            cursor.execute('''CREATE TABLE IF NOT EXISTS Clients (
                                Num_Client INT AUTO_INCREMENT PRIMARY KEY,
                                Nom VARCHAR(255),
                                Prenom VARCHAR(255),
                                Email VARCHAR(255),
                                MotDePasse VARCHAR(255),
                                Telephone VARCHAR(20)
                            )''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS Chambres (
                                Num_Chambre INT PRIMARY KEY,
                                Type VARCHAR(50),
                                Prix FLOAT,
                                Capacite INT,
                                Occupe BOOLEAN DEFAULT FALSE,
                                Date_Arrivee DATE,
                                Date_Depart DATE,
                                
                            )''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS Reservations (
                                Id INT AUTO_INCREMENT PRIMARY KEY,
                                Num_Client INT,
                                Num_Chambre INT,
                                Date_Arrivee DATE,
                                Date_Depart DATE,
                                Nombre_Nuits INT,
                                Nombre_Personnes INT,
                                Options TEXT,
                                FOREIGN KEY (Num_Client) REFERENCES Clients(Num_Client),
                                FOREIGN KEY (Num_Chambre) REFERENCES Chambres(Num_Chambre)
                            )''')

            conn.commit()
        else:
            print("Échec de la connexion à MySQL.")
    except Error as e:
        print("Erreur lors de la connexion à MySQL", e)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("La connexion MySQL est fermée.")

def inserer_chambres():
    # Connexion à la base de données
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        database='HotelRT'
    )
    cursor = conn.cursor()

    # Insertion des chambres Classic (101-109)
    for num_chambre in range(101, 110):
        cursor.execute('''
            INSERT INTO Chambres (Num_Chambre, Type, Prix, Capacite)
            VALUES (%s, %s, %s, %s)
        ''', (num_chambre, 'Classic', 30, 2))

    # Insertion des chambres Premium (201-209)
    for num_chambre in range(201, 210):
        cursor.execute('''
            INSERT INTO Chambres (Num_Chambre, Type, Prix, Capacite)
            VALUES (%s, %s, %s, %s)
        ''', (num_chambre, 'Premium', 60, 2))

    # Insertion des chambres Famille (301-309)
    for num_chambre in range(301, 310):
        cursor.execute('''
            INSERT INTO Chambres (Num_Chambre, Type, Prix, Capacite)
            VALUES (%s, %s, %s, %s)
        ''', (num_chambre, 'Famille', 150, 6))

    # Valider les insertions
    conn.commit()

    # Fermer la connexion
    cursor.close()
    conn.close()

def main():
    creer_base_de_donnees
    inserer_chambres()

if __name__=='__main__':
    main()