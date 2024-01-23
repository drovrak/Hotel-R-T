from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
import mysql.connector, hashlib
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton


Builder.load_file('existing_reservation_screen.kv')

def hacher_mot_de_passe(mot_de_passe):
    # Créer un objet de hachage MD5
    m = hashlib.md5()
    
    # Convertir le mot de passe en bytes et le hacher
    m.update(mot_de_passe.encode('utf-8'))
    
    # Obtenir la représentation hexadécimale du haché MD5
    mot_de_passe_hache = m.hexdigest()
    
    return mot_de_passe_hache
class RecapPopupContent(BoxLayout):
    recap_text = StringProperty('')
    
class ExistingReservationWidget(MDScreen,BoxLayout):
    def login(self, username, password):
        username = self.ids.username.text
        password = self.ids.mot_passe.text
    
    # Ici, ajoutez la logique pour vérifier les identifiants
        try:
        # Connexion à la base de données
            conn = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                password='root',
                database='HotelRT'
            )
            cursor = conn.cursor()

            # Requête pour vérifier les identifiants dans la table Clients
            mdp = hacher_mot_de_passe(password)  # Hacher le mot de passe

            cursor.execute("SELECT * FROM Clients WHERE Nom = %s AND MotDePasse = %s", (username, mdp))  # Utilisation de tuple pour les paramètres

            # Récupérer la première ligne de résultat
            result = cursor.fetchone()
            print(result)
            if result:
                nom = result[1]
                prenom = result[2]
                cursor.execute("SELECT * FROM Reservations WHERE Num_Client = %s", (result[0],))  # Utilisation de tuple pour les paramètres
                result = cursor.fetchone()
                date_arrivee = result[3]
                date_depart = result[4]
                num_chambre = result[2]
                cursor.execute("SELECT * FROM Chambres WHERE Num_Chambre = %s", (num_chambre,))  # Utilisation de tuple pour les paramètres
                result = cursor.fetchone()
                chambre = result[1]
                # Construire le texte du récapitulatif
                recap_text = f"Nom : {nom}\nPrénom : {prenom}\nDate de séjour : {date_arrivee} au {date_depart}\nChambre : {chambre}\nNuméro de chambre : {num_chambre}"
                self.show_recap_popup(recap_text)

            else:
                print("Identifiants invalides. L'utilisateur n'existe pas dans la base de données.")
                return False

        except mysql.connector.Error as error:
            print("Erreur lors de la vérification des identifiants : ", error)
            return False

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    
    def show_recap_popup(self,recap_text):
        # Créez une instance de MDDialog
        dialog = MDDialog(
            title='Récapitulatif des informations',
            text=recap_text,
            size_hint=(None, None),
            size=(400, 200)
        )

        # Ajoutez un bouton "Fermer" à la boîte de dialogue
        dialog.buttons = [
            MDRaisedButton(text="Fermer", on_release=lambda *x: dialog.dismiss())
        ]

        # Ouvrez la boîte de dialogue
        dialog.open()