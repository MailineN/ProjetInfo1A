"""Différentes fonctions des menus de l'application
"""
from pyfiglet import Figlet
from .menu_ouvert import Ouvert
from App.Functions.FonctionBD import clear

class Main_menu: 
    """Ensemble des méthodes définissant le menu principal et les enchainements de menus
    """    
    def __init__(self): 
        pass
    
    def Bienvenue(self):
        """ 
            Création du message de Bienvenue
            Se lance au lancement de l'application 
        """        
        clear()
        welcome = Figlet(font='big')
        print(welcome.renderText('Bienvenue'))
        print( )
        input("Appuyez sur Entrer pour lancer l'application : ")

        
    def Banner(self): 
        """[Non utilisée]
        """        
        print(" ʕᵔᴥᵔʔ ʕᵔᴥᵔʔ ʕᵔᴥᵔʔ ʕᵔᴥᵔʔ ʕᵔᴥᵔʔ ʕᵔᴥᵔʔ ʕᵔᴥᵔʔ ʕᵔᴥᵔʔ ʕᵔᴥᵔʔ ʕᵔᴥᵔʔ \n")
        print("\n")

    def Au_revoir(self): 
        """Création du message de départ de l'application
        """       
        clear() 
        print("\n")
        print(" ʕᵔᴥᵔʔ ʕᵔᴥᵔʔ ʕᵔᴥᵔʔ ʕᵔᴥᵔʔ ʕᵔᴥᵔʔ ʕᵔᴥᵔʔ ʕᵔᴥᵔʔ ʕᵔᴥᵔʔ ʕᵔᴥᵔʔ ʕᵔᴥᵔʔ \n")
        bye = Figlet(font='big')
        print(bye.renderText('Au  revoir'))

    def new_menu(self, previous_menu):
        """Affichage du menu actuel

        Arguments:
            previous_menu {list} -- Menu précédent permettant de revenir au menu

        Returns:
            vue_actuelle {list} -- Menu actuel
        """         
        vue_actuelle = Ouvert(previous_menu)
        while vue_actuelle:
            vue_actuelle = vue_actuelle.run()
        return vue_actuelle