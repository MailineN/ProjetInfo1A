"""Importation et traitement des données du fichier json 
"""### Importation des donnees ### 
import json
from FonctionBD import pays_vide


with open("App\Functions\DataTreatment\Country - Backup - FirstVer.json") as json_file:
    data = json.load(json_file)


### Tentative de suppression des valeurs manquantes ####

def clean_table(data):
    """Fonction permettant de réduire la taille de la base en retirant les pays qui ne possèdent pas l'intégralité des critères
    Ne garde également que les critères utilisés 

    Arguments:
        data {list of dict} -- Tableau de donnée original fourni
    
    Returns : 
        data_clean {list of dict} -- Base de donnée nettoyée 
    """    
    n=len(data)
    Table=[]
    for i in range(n):
        Intermed=11*[0]
        bool=True
        try:
            Intermed[0]= data[i]['Government']['Country name']['conventional short form']['text']
        except KeyError:
            bool=False
        try:
            Intermed[1]= data[i]['Geography']['Area']['total']['text']
        except KeyError:
            bool=False
        try:
            Intermed[2]= data[i]['People and Society']['Population']['text']
        except KeyError:
            bool=False
        try:
            Intermed[3]= data[i]['People and Society']['Population growth rate']['text']
        except KeyError:
            bool=False
        try:
            Intermed[4]= data[i]['Economy']['Inflation rate (consumer prices)']['text']
        except KeyError:
            bool=False
        try:
            Intermed[5]= data[i]['Economy']['Debt - external']['text']
        except KeyError:
            bool=False
        try:
            Intermed[6]= data[i]['Economy']['Unemployment rate']['text']
        except KeyError:
            bool=False
        try:
            Intermed[7]= data[i]['People and Society']['Health expenditures']['text']
        except KeyError:
            bool=False
        try:
            Intermed[8]= data[i]['People and Society']['Education expenditures']['text']
        except KeyError:
            bool=False
        try:
            Intermed[9]= data[i]['Military and Security']['Military expenditures']['text']
        except KeyError:
            bool=False
        try:
            Intermed[10]= data[i]['People and Society']['Age structure']
        except KeyError:
            bool=False
        if bool==True:
            Table.append(Intermed)  

    index_NA = [] #indices des pays possédant des valeurs manquantes
    for i in range(len(Table)):
        S = 0
        for j in range(len(Table[i])):
            if 'NA' in Table[i][j]:
                S = 1
        if S == 1:
            index_NA.append(i)        

    liste_pays = []
    for i in range(len(index_NA)):
        liste_pays.append(Table[index_NA[i]][0])

    for j in range(len(liste_pays)):
        index = -1
        for i in range(len(Table)):
            if liste_pays[j] == Table[i][0]:
                index = i
        if index > -1:
            Table.pop(index)       
    

    data_clean = []
    for i in range(len(Table)): 
        entree = pays_vide()
        entree['Government']['Country name']['conventional short form']['text'] = Table[i][0]
        entree['Geography']['Area']['total']['text'] = Table[i][1]
        entree['People and Society']['Population']['text'] = Table[i][2]
        entree['People and Society']['Population growth rate']['text'] = Table[i][3]
        entree['Economy']['Inflation rate (consumer prices)']['text'] = Table[i][4]
        entree['Economy']['Debt - external']['text'] = Table[i][5]
        entree['Economy']['Unemployment rate']['text'] = Table[i][6]
        entree['People and Society']['Health expenditures']['text'] = Table[i][7]
        entree['People and Society']['Education expenditures']['text'] = Table[i][8]
        entree['Military and Security']['Military expenditures']['text'] = Table[i][9]
        entree['People and Society']['Age structure'] = Table[i][10]
        data_clean.append(entree)

    return(data_clean)

data_clean = clean_table(data) 

with open("App\Functions\DataTreatment\country.json", "w") as write_file:
    json.dump(data_clean, write_file)





