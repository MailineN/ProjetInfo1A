"""Fichier principal permettant de lancer l'application 
"""
from App.Menus import main_menu as menu_principal
from App.Menus import menu as menu_option


if __name__ == '__main__':
    """Lancement de l'application avec test préalable du bon fichier 
    """    
    menus = menu_principal.Main_menu()
    menus.Bienvenue()
    menus.new_menu(menu_option.menu[0])
    menus.Au_revoir()

