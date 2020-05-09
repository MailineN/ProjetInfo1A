"""Déroulement des menus en partant du menu principal et fonctions annexes sur les menus 
"""

from Acteurs import Individu
from Acteurs import Consultant
from Acteurs import Geographe
from Acteurs import DataScientist
from Acteurs import Admin
from Menus.menu_ouvert import Ouvert


def connexion(previous_menu): 
    """Menu intermédiaire de connection proposant à l'utilisateur de se connecter s'il ne l'est pas 

    Arguments:
        previous_menu {liste} -- Menu précédent de l'utilisateur spécifié 
    """    
    menu_act = previous_menu

    if menu_act["individu"].connexion() : #Vérifie si l'acteur peut se connecter et est connecté  
        # On retire à l'utilisateur la possibilité de se co
        del menu_act["options"][0] 
        del menu_act["actions"][0]
    
    return(Ouvert(menu_act))

def indices_actions(ind,indice_taches):
    """Définit les actions possibles pour chaques classes dans le menu 
    Différent des indices d'appel de critère utilisés dans certaines fonctions

    Arguments:
        ind {Individu.class} -- Individu spécifié ayant des actions propres
        indice_taches {List} -- Liste des toutes les taches possibles
    """    
    menu_act = {}
    menu_act["individu"] = ind
    menu_act["question"] = menu[1]["question"]
    menu_act["options"] = [menu[1]["options"][i] for i in indice_taches]
    menu_act["actions"] = [menu[1]["actions"][i] for i in indice_taches]
    menu_act["path"] = []
    return(Ouvert(menu_act))

def menu_graph(previous_menu): 
    """Création du menu intermédaire pour la fonction représentation graphique 

    Arguments:
        previous_menu {List} -- Menu précédent correspondant à l'utilisateur 
    """    
    menu_act = {}
    menu_act["individu"] = previous_menu["individu"]
    menu_act["question"] = "Selectionnez le critère"
    menu_act["options"] = ["Superficie", #2
        "Population", #3
        "Croissance démographique", #4
        "Inflation", #5
        "Dette", #6
        "Taux de chômage", #7
        "Taux de dépenses en santé", #8
        "Taux de dépenses en éducation", #9
        "Taux de dépenses militaires", #10
        "Retour au menu principal", 
        "Quitter l'application"]
    menu_act["actions"] = [
            (lambda previous_menu :previous_menu["individu"].representationgraphique(previous_menu,1)),
            (lambda previous_menu :previous_menu["individu"].representationgraphique(previous_menu,2)),
            (lambda previous_menu :previous_menu["individu"].representationgraphique(previous_menu,3)), # 
            (lambda previous_menu :previous_menu["individu"].representationgraphique(previous_menu,4)),
            (lambda previous_menu :previous_menu["individu"].representationgraphique(previous_menu,5)),
            (lambda previous_menu :previous_menu["individu"].representationgraphique(previous_menu,6)),
            (lambda previous_menu :previous_menu["individu"].representationgraphique(previous_menu,7)),
            (lambda previous_menu :previous_menu["individu"].representationgraphique(previous_menu,8)),
            (lambda previous_menu :previous_menu["individu"].representationgraphique(previous_menu,9)),
            (lambda previous_menu : Ouvert(menu[0])),
            Individu().quitter]
    menu_act["path"] = []
    
    return(Ouvert(menu_act))

def menu_resume(previous_menu): 
    """Création du menu intermédaire pour la fonction résumé d'information

    Arguments:
        previous_menu {List} -- Menu précédent correspondant à l'utilisateur 
    """ 
    menu_act = {}
    menu_act["individu"] = menu_act["individu"] = previous_menu["individu"]
    menu_act["question"] = "Selectionnez le critère"
    menu_act["options"] = ["Superficie", #2
        "Population", #3
        "Croissance démographique", #4
        "Inflation", #5
        "Dette", #6
        "Taux de chômage", #7
        "Taux de dépenses en santé", #8
        "Taux de dépenses en éducation", #9
        "Taux de dépenses militaires", 
        "Classes d'âges", 
        "Retour au menu principal", 
        "Quitter l'application"]
    menu_act["actions"] = [
            (lambda previous_menu :previous_menu["individu"].resume('total',previous_menu)),
            (lambda previous_menu :previous_menu["individu"].resume('Population',previous_menu)),
            (lambda previous_menu :previous_menu["individu"].resume('Population growth rate',previous_menu)), # 
            (lambda previous_menu :previous_menu["individu"].resume('Inflation rate (consumer prices)',previous_menu)),
            (lambda previous_menu :previous_menu["individu"].resume('Debt - external',previous_menu)),
            (lambda previous_menu :previous_menu["individu"].resume('Unemployment rate',previous_menu)),
            (lambda previous_menu :previous_menu["individu"].resume('Health expenditures',previous_menu)),
            (lambda previous_menu :previous_menu["individu"].resume('Education expenditures',previous_menu)),
            (lambda previous_menu :previous_menu["individu"].resume('Military expenditures',previous_menu)),
            menu_age,
            (lambda previous_menu : Ouvert(menu[0])),
            Individu().quitter]
    menu_act["path"] = []
    
    return(Ouvert(menu_act))

def menu_age(previous_menu): 
    """Création du menu intermédaire pour les tranches d'age pour la fonction résumé d'information

    Arguments:
        previous_menu {List} -- Menu précédent correspondant à l'utilisateur 
    """ 
    menu_act = {}
    menu_act["individu"] = menu_act["individu"] = previous_menu["individu"]
    menu_act["question"] = "Selectionnez la tranche d'âge"
    menu_act["options"] = ["0-14 ans", #2
        "15-24 ans", #3
        "25-54 ans", #4
        "55-64 ans", #5
        "65 ans et plus", #6
        "Retour au menu principal",
        "Quitter l'application"]
    menu_act["actions"] = [
            (lambda previous_menu :previous_menu["individu"].resume('0-14 years',previous_menu)),
            (lambda previous_menu :previous_menu["individu"].resume('15-24 years',previous_menu)),
            (lambda previous_menu :previous_menu["individu"].resume('25-54 years',previous_menu)), # 
            (lambda previous_menu :previous_menu["individu"].resume('55-64 years',previous_menu)),
            (lambda previous_menu :previous_menu["individu"].resume('65 years and over',previous_menu)),
            (lambda previous_menu : Ouvert(menu[0])),
            Individu().quitter]
    menu_act["path"] = []
    return(Ouvert(menu_act))

def gestion_pays(previous_menu):
    """Menu intermédiare permettant à l'utilisateur de choisir entre l'ajout et la suppréssion de pays 

    Arguments:
        previous_menu {List} -- Menu précédent correspondant à l'utilisateur 
    """    
    menu_act = {}
    menu_act["individu"] = previous_menu["individu"]
    menu_act["question"] = "Que voulez vous faire ? "
    menu_act["options"] = ["Ajouter/Modifier un pays",
        "Supprimer un pays (Administrateur seulement) ", 
        "Retour au menu précédent", 
        "Quitter l'application"]
    menu_act["actions"] = [
            (lambda previous_menu :previous_menu["individu"].ajout_pays(previous_menu)),
            (lambda previous_menu :previous_menu["individu"].suppression(previous_menu)),
            (lambda previous_menu : Ouvert(menu[0])),
            Individu().quitter]
    menu_act["path"] = []
    return(Ouvert(menu_act))

def gestion_comptes(previous_menu):
    """Menu intermédiare permettant à l'utilisateur de choisir entre l'ajout et la suppression de comptes

    Arguments:
        previous_menu {List} -- Menu précédent correspondant à l'utilisateur 
    """    
    menu_act = {}
    menu_act["individu"] = previous_menu["individu"]
    menu_act["question"] = "Que voulez vous faire ? "
    menu_act["options"] = ["Créer un compte Géographe/DataScientist",
        "Supprimer un compte ", 
        "Retour au menu principal", 
        "Quitter l'application"]
    menu_act["actions"] = [
            (lambda previous_menu :previous_menu["individu"].ajout_compte(previous_menu)),
            (lambda previous_menu :previous_menu["individu"].suppression_compte(previous_menu)),
            (lambda previous_menu : Ouvert(menu[0])),
            Individu().quitter]
    menu_act["path"] = []
    return(Ouvert(menu_act))

def menu_clust(previous_menu):
    """Menu intermédiare permettant à l'utilisateur de choisir la méthode de clustering à utiliser 
    Arguments:
        previous_menu {List} -- Menu précédent correspondant à l'utilisateur 
    """    
    menu_act = {}
    menu_act["individu"] = previous_menu["individu"]
    menu_act["question"] = "Quelle méthode voulez vous utiliser ? \nNote : L'Inde a été retirée de la base de donnée afin de clarifier les résultats "
    menu_act["options"] = ["Clustering par méthode CAH",
        "Clustering par méthode des K-means", 
        "Retour au menu principal", 
        "Quitter l'application"]
    menu_act["actions"] = [
            (lambda previous_menu :previous_menu["individu"].clust('CAH',previous_menu)),
            (lambda previous_menu :previous_menu["individu"].clust('K-means',previous_menu)),
            (lambda previous_menu : Ouvert(menu[0])),
            Individu().quitter]
    menu_act["path"] = []
    return(Ouvert(menu_act))

menu = [
    { 
        "question" : "Selectionnez votre type utilisateur",
        "options" : ["Consultant", "Géographe", "DataScientist", "Administrateur", "Quitter l'application"],
        "actions" : [
            (lambda previous_menu :indices_actions(Consultant(),[1,4,9,10])),
            (lambda previous_menu :indices_actions(Geographe(),[0,1,5,6,9,10])),
            (lambda previous_menu :indices_actions(DataScientist(),[0,1,2,3,4,8,9,10])),
            (lambda previous_menu :indices_actions(Admin(),[0,1,2,3,5,6,7,8,9,10])),
            Individu().quitter],
        "individu": Individu(),
        "path": []
    },


    {
        "question" : "Que voulez vous faire ? ",
        "options" : ["Connexion", #0
        "Affichage de données pays", #1
        "Représentation graphique", #2 Data
        "Résumés statistiques", #3 Data
        "Proposition suggestion", #4
        "Gestion des pays", #5
        "Gestion des suggestions", #6
        "Gestion des comptes",
        "Clustering", #7
        "Retour au menu précédent", #8
        "Quitter l'application"],#9
        "actions" : [connexion,
            (lambda previous_menu :previous_menu["individu"].affichage(previous_menu)),
            menu_graph,
            menu_resume, # à faire 
            (lambda previous_menu :previous_menu["individu"].ajout_suggestion(previous_menu)),
            gestion_pays,
            (lambda previous_menu :previous_menu["individu"].gestion_suggestion(previous_menu)),
            gestion_comptes,
            menu_clust,
            (lambda previous_menu :Ouvert(menu[0])),
            Individu().quitter],
        "individu": Individu(),
        "path": []
    }]
"""Menu principal et menu utilisateur proposant l'ensemble des actions possibles
"""
