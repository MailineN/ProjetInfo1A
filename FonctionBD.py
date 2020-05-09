""" 
Ce fichier regroupe toutes les fonctionnalités annexes utilisées dans l'application 
afin de ne pas surcharger le module Acteurs et pouvant être utilisées égalements dans les menus ou le traitement de données  

""" 


import matplotlib.pyplot as plt
import json
import numpy
import os

# Fonction permettant de vider la console 

clear = lambda: os.system('cls') 
"""Fonction permettant de supprimer la console afin d'avoir un menu propre
"""

#### FICHIER DE REGROUPEMENT DES FONCTIONS ANNEXES ####

def pays_vide():  
    """Genere un pays vide contenant uniquement les critères utilises dans l'application

    Returns:
        entree{list of dict} -- Pays vide 

    """     

    entree = {}
    entree['Government'] = {}
    entree['Government']['Country name'] = {}
    entree['Government']['Country name']['conventional short form']={}

    entree['People and Society'] = {}
    entree['People and Society']['Population'] = {}
    entree['People and Society']['Population growth rate']={}
    entree['People and Society']['Health expenditures']={}
    entree['People and Society']['Education expenditures']={}

    entree['Military and Security'] ={}
    entree['Military and Security']['Military expenditures']={}

    entree['People and Society']['Age structure'] = {}
    entree['People and Society']['Age structure']['0-14 years'] = {}
    entree['People and Society']['Age structure']['15-24 years'] = {}
    entree['People and Society']['Age structure']['25-54 years'] = {}
    entree['People and Society']['Age structure']['55-64 years'] = {}
    entree['People and Society']['Age structure']['65 years and over'] = {}

    entree['Economy'] = {}
    entree['Economy']['Inflation rate (consumer prices)'] = {}
    entree['Economy']['Debt - external'] = {}
    entree['Economy']['Unemployment rate'] = {}

    entree['Geography'] = {}
    entree['Geography']['Area'] = {}
    entree['Geography']['Area']['total'] = {}

    return(entree)

# Fonction test d'un nombre ou d'une chaîne de caractère
def is_number(s):
    """ Teste si la variable entrée est un nombre

    Arguments:
        s {int,float,str} -- variable à tester

    Returns:
        {bool} -- Test vérifié ou non 
    """    
    try:
        float(s)
        return True
    except ValueError:
        return False

# Fonction de récupération de code pays 
def get_code(nom_pays): 
    """Permet de récuperer le code d'un pays dans la base de donnée utilisateur User.json

    Arguments:
        nom_pays {str} -- Nom du pays à récupérer

    Raises:
        NameError: Le pays n'est pas dans la base
    """
    with open("DataTreatment/country.json") as json_file: 
        data =json.load(json_file)    

    code = ''
    for code_pays in range(len(data)) :
        code = ''
        # On verifie la presence des noms à chaque etape

        if data[code_pays].get('Government') : 
            if data[code_pays]['Government'].get('Country name') :
                if data[code_pays]['Government']['Country name'].get('conventional long form') :
                    if data[code_pays]['Government']['Country name']['conventional long form']['text'] == nom_pays :
                        code = code_pays
                        
                        break
                if data[code_pays]['Government']['Country name'].get('conventional short form') :
                    if data[code_pays]['Government']['Country name']['conventional short form']['text'] == nom_pays :
                        code = code_pays
                        
                        break
                if data[code_pays]['Government']['Country name'].get('local long form') :
                    if data[code_pays]['Government']['Country name']['local long form']['text'] == nom_pays :
                        code = code_pays
                        
                        break
                if data[code_pays]['Government']['Country name'].get('local short form') :
                    if data[code_pays]['Government']['Country name']['local short form']['text'] == nom_pays :
                        code = code_pays
                        
                        break

    if code == '' :
        raise NameError('Pays introuvable')
    else :
        return(code)

# Fonction de création de listes 
# liste des comptes 
def account_list(users): 
    """Permet de récupérer la liste des utilisateurs dans la base de donnée utilisateur User.json

    Arguments:
        users {list of dict} -- Base de données utilisateurs
    """    
    liste =[]
    for i in users : 
        liste.append(i['ID']['username'])
    return(liste)

def password_list(users): 
    """Permet de récupérer la liste des mots de passes dans la base de donnée utilisateur User.json

    Arguments:
        users {list of dict} -- Base de données utilisateurs
    """    
    liste =[]
    for i in users : 
        liste.append(i['ID']['mdp'])
    return(liste)

def type_liste(users): 
    """Permet de récupérer la liste des types par utilisateurs dans la base de donnée utilisateur User.json

    Arguments:
        users {list of dict} -- Base de données utilisateurs
    """    
    liste =[]
    for i in users : 
        liste.append(i['type'])
    return(liste)
