from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from send import inserer_donnees_json
import hashlib

import json, random

# Chargement du fichier KV pour la mise en page de l'interface utilisateur
Builder.load_file('new_reservation_screen.kv')


class ReservationWidget(MDScreen):
    # Déclaration des propriétés ObjectProperty pour les widgets interactifs
    #Premier screen
    nom = ObjectProperty(None)
    prenom = ObjectProperty(None)
    email = ObjectProperty(None)
    telephone = ObjectProperty(None)
    #2 screen
    mot_passe = ObjectProperty(None)
    conf_mot_passe = ObjectProperty(None)
    #3 screen
    nbrNuit = ObjectProperty(None)
    TypeChambre = ObjectProperty(None)
    nbrPersonnes = ObjectProperty(None)
    nbrDej = ObjectProperty(None)
    #troisieme screen
    option = ObjectProperty(None)

        
    def show_date_picker(self):
        """
        Affiche un sélecteur de dates permettant à l'utilisateur de choisir une plage de dates.
        """
        date_dialog = MDDatePicker(mode="range")
        date_dialog.bind(on_save=self.on_date_range_save, on_cancel=self.on_cancel_date_picker)
        date_dialog.open()
        
    def on_date_range_save(self, picker, start_date, end_date):
        """
        Callback appelé lors de la sauvegarde d'une plage de dates. Met à jour les champs d'arrivée et de départ,
        ainsi que le nombre de nuits et de petits-déjeuners basé sur la sélection.
        """
        self.ids.arrival_date.text = str(start_date)
        self.ids.departure_date.text = str(end_date[-1])
        delta = end_date[-1] - start_date
        self.ids.nbr_nuit.text = str(delta.days)  # Mettre à jour le champ nbr_nuit
        self.ids.nbr_dej.text = str(delta.days)

    def on_cancel_date_picker(self, *args):
        """
        Callback appelé lorsque l'utilisateur annule la sélection de la date.
        """
        print("Sélection de date annulée")
        
    def __init__(self, **kwargs):
        """
        Initialise le widget avec un menu déroulant pour sélectionner le type de chambre.
        """
        super(ReservationWidget, self).__init__(**kwargs)
        self.menu_items = [
            {"text": f"{i}", "viewclass": "OneLineListItem", "on_release": lambda x=f"{i}": self.set_item(x)}
            for i in ["Classic", "Premium", "Famille"]
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.type_chambre,
            items=self.menu_items,
            width_mult=2
        )
        self.ids.nbr_pers.bind(text=self.on_nbr_pers_change)  # Use the correct widget name

    def on_nbr_pers_change(self, instance, value):
        self.update_chambre_options()

    def update_chambre_options(self):
        """
        Met à jour les options de type de chambre en fonction du nombre de personnes.
        """
        nbr_personnes = int(self.ids.nbr_pers.text) if self.ids.nbr_pers.text.isdigit() else 0  # Use the correct widget name

        if nbr_personnes <= 2:
            chambre_options = ["Classic", "Premium"]
        elif nbr_personnes <= 6:
            chambre_options = ["Famille"]
        else:
            chambre_options = []  # Aucune option si le nombre de personnes dépasse la capacité maximale

        self.menu_items = [{"text": f"{i}", "viewclass": "OneLineListItem", "on_release": lambda x=f"{i}": self.set_item(x)} for i in chambre_options]
        self.menu.items = self.menu_items
        if chambre_options:
            self.ids.type_chambre.text = chambre_options[0]  # Mettre à jour le texte par défaut avec la première option
        else:
            self.ids.type_chambre.text = "Aucune option disponible"
        
    def toggle_password_visibility(self, textfield):
        textfield.password = not textfield.password
        textfield.icon_right = "eye" if not textfield.password else "eye-off"

    def set_item(self, text):
        """
        Définit l'élément sélectionné dans le menu déroulant pour le type de chambre.
        """
        self.ids.type_chambre.text = text
        self.menu.dismiss()


    def submit(self):
        """
        Rassemble toutes les données du formulaire et les enregistre dans un fichier JSON.
        """
        reservation_id = str(self.ids.nom.text) + str(random.randint(1000, 9999))
        mot_de_passe = self.ids.mot_passe.text
        mot_de_passe = hacher_mot_de_passe(mot_de_passe)
        options = {
            "TV": self.ids.option_tv.active,
            "Minibar": self.ids.option_minibar.active,
            "Balcon": self.ids.option_balcon.active,
            "Parking": self.ids.option_parking.active
        }
        data = {
            "id": reservation_id, 
            "Nom": self.ids.nom.text,
            "Prenom": self.ids.prenom.text,
            "Email": self.ids.email.text,
            "MotDePasse": mot_de_passe,
            "Telephone": self.ids.telephone.text,
            "Date_arrivee": self.ids.arrival_date.text,
            "Date_depart": self.ids.departure_date.text,
            "Nombre_Nuit": self.ids. nbr_nuit.text,
            "Type_Chambre": self.ids.type_chambre.text,
            "Nombre_personnes": self.ids.nbr_pers.text,
            "Nombre_petit-dej": self.ids.nbr_dej.text,
            "Options": options
        }
        self.save_to_json(data)
        inserer_donnees_json('reservation_data.json')

    def save_to_json(self, data):
        """
        Sauvegarde les données du formulaire dans un fichier JSON.
        """
        with open('reservation_data.json', 'w') as file:
            json.dump(data, file, indent=4)
def hacher_mot_de_passe(mot_de_passe):
    # Créer un objet de hachage MD5
    m = hashlib.md5()
    
    # Convertir le mot de passe en bytes et le hacher
    m.update(mot_de_passe.encode('utf-8'))
    
    # Obtenir la représentation hexadécimale du haché MD5
    mot_de_passe_hache = m.hexdigest()
    
    return mot_de_passe_hache
