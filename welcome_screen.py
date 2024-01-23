from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from new_reservation_screen import ReservationWidget
from existing_reservation_screen import  ExistingReservationWidget

# Charger les fichiers KV pour les différentes interfaces utilisateur de l'application
Builder.load_file('welcome_screen.kv')
Builder.load_file('new_reservation_screen.kv')
Builder.load_file('existing_reservation_screen.kv')

class WelcomeScreen(Screen):
    """
    Écran d'accueil de l'application. 
    Cet écran est le point de départ et peut contenir des liens vers d'autres écrans.
    """
    pass

class NewReservationScreen(Screen):
    """
    Écran pour créer une nouvelle réservation.
    Il intègre le widget ReservationWidget défini dans new_reservation_screen.py.
    """
    def __init__(self, **kwargs):
        super(NewReservationScreen, self).__init__(**kwargs)
        # Ajouter le widget de réservation à cet écran
        self.add_widget(ReservationWidget()) 

class ExistingReservationScreen(Screen):
    """
    Écran pour afficher et gérer les réservations existantes.
    Cet écran peut être utilisé pour afficher une liste des réservations précédentes.
    """
    def __init__(self, **kwargs):
        super(ExistingReservationScreen, self).__init__(**kwargs)
         # Ajouter le widget de réservation à cet écran
        self.add_widget(ExistingReservationWidget()) 

class MyApp(MDApp):
    """
    Classe principale de l'application. Gère l'initialisation de l'application et la configuration du ScreenManager.
    """
    def build(self):
        # Définir le style et la palette de couleurs du thème de l'application
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"

        # Définir la taille de la fenêtre principale de l'application
        Window.size = (800, 950)

        # Création du ScreenManager pour gérer les différents écrans
        sm = ScreenManager()    
        # Ajout des écrans au ScreenManager
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(NewReservationScreen(name='new_reservation'))
        sm.add_widget(ExistingReservationScreen(name='existing_reservation'))

        return sm
    
    def go_back_to_welcome(self):
        # Cette méthode change l'écran actuel en 'welcome' avec une transition vers la gauche
        self.sm.transition.direction = 'right'  # Transition vers la gauche lorsque vous revenez en arrière
        self.sm.current = 'welcome'
        self.sm.transition.direction = 'left'  # Réinitialise la direction pour les autres transitions

if __name__ == '__main__':
    MyApp().run()
