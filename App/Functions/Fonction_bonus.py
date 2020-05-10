"""Fonction bonus de l'application. 
Elle consiste à la réalisation d'un clustering sur les données de l'application

Raises:
    Exception: L'erreur d'argument indique que l'utilisateur a outrepassé les menus, normalement impossible


"""
import pandas as pd
import json
import numpy as np 
import matplotlib.pyplot as plt
from sklearn import cluster
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.preprocessing import StandardScaler 
from sklearn.decomposition import PCA
from sklearn import metrics
#générer la matrice des liens

def clustering(methode):
    def to_df():
        """Transforme la base de donnée json en dataframe plus adaptée pour le clustering 
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

    df,pays = to_df()


    # Clustering CAH
    def clust_CAH(df,pays):
        Z = linkage(df,method='ward',metric='euclidean')
        #affichage du dendrogramme
        plt.title("CAH")
        dendrogram(Z,labels=pays,orientation='left',color_threshold=1.5*(10**7))
        plt.show() 

    #clustering K-means
    def clust_Kmeans(df,pays):
        ss = StandardScaler()
        ss.fit_transform(df)
        
        kmeans = cluster.KMeans(n_clusters=4).fit(df)

        acp = PCA(n_components=2).fit_transform(df)

        for couleur,k in zip(['sandybrown','lightskyblue','palegreen'],[0,1,2]):
            plt.scatter(acp[kmeans.labels_==k,0],acp[kmeans.labels_==k,1],c=couleur,s=50, alpha=0.5)
        plt.title('Clustering par Methode des K-Means')
        plt.xlabel('Axe factoriel 1')
        plt.ylabel('Axe factoriel 2')
        plt.show() 

    if methode =='CAH' : 
        clust_CAH(df,pays)
        input("\nAffichage terminé, appuyez sur Entrer pour continuer ")
    elif methode == 'K-means': 
        clust_Kmeans(df,pays)
        input("\nAffichage terminé, appuyez sur Entrer pour continuer ")
    else : 
        raise Exception("Argument invalide, l'application est cassée")

if __name__ == '__main__':
    clustering('K-means') 