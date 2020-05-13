""" 
Ce fichier regroupe toutes les fonctionnalités annexes utilisées dans l'application 
afin de ne pas surcharger le module Acteurs et pouvant être utilisées égalements dans les menus ou le traitement de données  

""" 

import pandas as pd
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
    with open(r"App\Functions\DataTreatment\country.json") as json_file: 
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

def to_df():
        """Transforme la base de donnée json en dataframe plus adaptée pour le clustering et pour le résumé Statistique
        Retire le pays 'Inde' qui pose problème 

        Returns:
            df {pandas dataframe} -- Dataframe contenant les informations pays 
            pays {list} -- Liste des pays 
        """    

        with open(r"App\Functions\DataTreatment\country.json") as json_file:
            data = json.load(json_file)     

        pays=[]         
        tranche1=[]
        tranche2=[]
        tranche3=[]
        tranche4=[]
        tranche5=[]
        infl = []
        area = []
        hab = []
        growth = []
        debt = []
        unemploy = []
        healthcare = []
        education = []
        military = []

        #Récupération des données numériques
        for j in range (len(data)):
            pays.append(data[j]['Government']['Country name']['conventional short form']['text'])

            superficie = data[j]['Geography']['Area']['total']['text']
            superficie = superficie[:superficie.find(' s')]
            superficie = superficie.replace( ',' , '' )    
            area.append(float(superficie))

            pop = data[j]['People and Society']['Population']['text']
            pop = pop[:pop.find(' (')]
            pop = pop[:pop.find(' m')]
            pop = pop.replace( ',' , '' )
            hab.append(float(pop))

            pourcent = data[j]['People and Society']['Population growth rate']['text']
            pourcent = pourcent[:pourcent.find('%')]   
            growth.append(float(pourcent)) 

            dette=data[j]['Economy']['Debt - external']['text']                
            dette=dette[:dette.find(' (')]
            dette=dette.replace('$','')
            dette=dette.replace(' million','')
            dette=dette.replace(' billion','e3')
            dette=dette.replace(' trillion','e6')
            debt.append(float(dette))

            pourcent = data[j]['Economy']['Inflation rate (consumer prices)']['text']                    
            inf2016 = pourcent[:pourcent.find('%')]                  
            infl.append(float(inf2016))  

            taux=data[j]['Economy']['Unemployment rate']['text']
            taux=taux[:taux.find(' ++')]
            taux = taux[:taux.find('%')]
            unemploy.append(float(taux))

            pourcent = data[j]['People and Society']['Health expenditures']['text']                  
            pourcent = pourcent[:pourcent.find('%')]
            healthcare.append(float(pourcent))

            dep=data[j]['People and Society']['Education expenditures']['text']                
            dep=dep[:dep.find('%')]
            education.append(float(dep))

            dep=data[j]['Military and Security']['Military expenditures']['text']
            dep=dep[:dep.find(' ++')]
            dep=dep[:dep.find('%')]
            military.append(float(dep)) 

            tranche1.append(data[j]['People and Society']['Age structure']['0-14 years']['text'])
            tranche2.append(data[j]['People and Society']['Age structure']['15-24 years']['text'])
            tranche3.append(data[j]['People and Society']['Age structure']['25-54 years']['text'])
            tranche4.append(data[j]['People and Society']['Age structure']['55-64 years']['text'])
            tranche5.append(data[j]['People and Society']['Age structure']['65 years and over']['text'])

            TR1=[]
            for z in range(len(tranche1)):
                TR1.append(float(tranche1[z][:tranche1[z].find('%')]))
                                
            TR2=[]
            for z in range(len(tranche2)):
                TR2.append(float(tranche2[z][:tranche2[z].find('%')]))
            
            TR3=[]
            for z in range(len(tranche3)):
                TR3.append(float(tranche3[z][:tranche3[z].find('%')]))    
            
            TR4=[]
            for z in range(len(tranche4)):
                TR4.append(float(tranche4[z][:tranche4[z].find('%')]))    
        
            TR5=[]
            for z in range(len(tranche5)):
                TR5.append(float(tranche5[z][:tranche5[z].find('%')]))

        Data = {
            'Superficie' : area,
            'Population' : hab,
            'Croissance démographique' : growth,
            'Inflation' : infl,
            'Dette' : debt,
            'Taux de chômage' : unemploy,
            'Taux de dépense en santé' : healthcare,
            'Taux de dépense en éducation' : education,
            'Taux de dépense militaire' : military,
            'Classe des 0-14 ans': TR1,
            'Classe des 15-24 ans': TR2,
            'Classe des 25-54 ans': TR3,
            'Classe des 55-64 ans': TR4,
            'Classe des plus de 65 ans': TR5,
        }
        
        df = pd.DataFrame(Data,columns=[
            'Superficie',
            'Population',
            'Croissance démographique',
            'Inflation',
            'Dette',
            'Taux de chômage',
            'Taux de dépense en santé',
            'Taux de dépense en éducation',
            'Taux de dépense militaire',
            'Classe des 0-14 ans',
            'Classe des 15-24 ans',
            'Classe des 25-54 ans',
            'Classe des 55-64 ans',
            'Classe des plus de 65 ans'])

        df=df.drop(pays.index('India'))
        pays.remove('India')
        return (df,pays)

