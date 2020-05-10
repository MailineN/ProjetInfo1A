"""Fonction bonus de l'application. 
Elle consiste à la réalisation d'un clustering sur les données de l'application.

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
from App.Functions.FonctionBD import to_df
#générer la matrice des liens

class clustering:
    """Classe regroupant les méthodes de clustering, ici le CAH et les K-means
    """    
    def __init__(self): 
        """Transformation de la base de donnée initiale en pandas df afin de faire le clustering plus facilement
        """        
        self.df,self.pays=to_df()


    def clust_CAH(self):
        """Réalisation d'un clustering selon la méthode du CAH

        Arguments:
            self {clustering.class} -- jeu de données utilisées pour le clustering 
        """        
        Z = linkage(self.df,method='ward',metric='euclidean')
        #affichage du dendrogramme
        plt.title("CAH")
        dendrogram(Z,labels=self.pays,orientation='left',color_threshold=1.5*(10**7))
        plt.show() 

    def clust_Kmeans(self):
        """Réalisation d'un clustering selon la méthode du CAH

        Arguments:
            self {clustering.class} -- jeu de données utilisées pour le clustering 
        """    
        ss = StandardScaler()
        ss.fit_transform(self.df)
        
        kmeans = cluster.KMeans(n_clusters=4).fit(self.df)

        acp = PCA(n_components=2).fit_transform(self.df)

        for couleur,k in zip(['sandybrown','lightskyblue','palegreen'],[0,1,2]):
            plt.scatter(acp[kmeans.labels_==k,0],acp[kmeans.labels_==k,1],c=couleur,s=50, alpha=0.5)
        plt.title('Clustering par Methode des K-Means')
        plt.xlabel('Axe factoriel 1')
        plt.ylabel('Axe factoriel 2')
        plt.show() 

