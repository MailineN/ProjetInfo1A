    # Importation des donnees

import json
import pandas as pd
from . import FonctionBD as fbd

class Affichage_Stat: 
    def __init__(self):

        with open(r"App\Functions\DataTreatment\country.json") as json_file:
            self.data = json.load(json_file)

        # On modifie pour la pop d'Israeal car la phrase fait que le code ne marche pas
        self.data[47]['People and Society']['Population']['text'] = '8,174,527 (July 2016 est.)'


    # Fonction resume

    def tri_croissant(self,critere):
        while True : 
            nb_pays_max = input("Entrez le nombre de pays que vous voulez observer : ")
            if fbd.is_number(nb_pays_max): 
                break
        # Fonction qui trouve quel est le chemin pour acceder au critere demandé

        def chemin(critere) :

            chemin_critere = []

            code_pays = 0
            while code_pays < len(self.data) and chemin_critere == [] :
                for a in self.data[code_pays] :
                    if a == critere :
                        chemin_critere = [a]
                    else :
                        if a != 'text' :
                            for b in self.data[code_pays][a] :
                                if b == critere :
                                    chemin_critere = [a,b]
                                else :
                                    if b != 'text' :
                                        for c in self.data[code_pays][a][b] :
                                            if c == critere :
                                                chemin_critere = [a,b,c]
                code_pays += 1

            return chemin_critere

        # Determination du chemin pour accéder au critere
        chemin = chemin(critere)

        # Est ce que le dernier critere est atteint ? Sinon, on le choisit :

        test_text = False
        if len(chemin) == 1 :
            for suite in self.data[0][chemin[0]] :
                if str(suite) == 'text' :
                    test_text = True
            if not test_text :
                for suite in self.data[0][chemin[0]] :
                    print(suite)
                choix_dernier_critere = input('Choisissez le critere voulu (par exemple : ecrire total et non "total") :')
                chemin += [choix_dernier_critere]

        test_text = False
        if len(chemin) == 2 :
            for suite in self.data[0][chemin[0]][chemin[1]] :
                if str(suite) == 'text' :
                    test_text = True
            if not test_text :
                for suite in self.data[0][chemin[0]][chemin[1]] :
                    print(suite)
                choix_dernier_critere = input('Choisissez le critere voulu (par exemple : ecrire total et non "total") :')
                chemin += [choix_dernier_critere]

        if chemin == [] :
            raise NameError('Critère non reconnu')
            # Critere qui n'est pas dans la base de données

        if nb_pays_max > 10:
            raise NameError('Nombre de pays demandés trop élevé')
            # Erreur car nombre de pays demandés trop élevé


        # Fonction qui donne l'information associée à un critere et à un pays

        def information_pays(code_pays) :

            if len(chemin) == 1 :
                return self.data[code_pays][chemin[0]]['text']
            elif len(chemin) == 2 :
                return self.data[code_pays][chemin[0]][chemin[1]]['text']
            else :
                return self.data[code_pays][chemin[0]][chemin[1]][chemin[2]]['text']



        # L'utilisateur doit il choisir l'information qui l'intéresse ? Pour cela comptons les valeurs dans l'information

        # On comte le nombre n de valeurs dans les informations et on garde le max
        n_max = 0

        for code_pays in range(len(self.data)) :

            n = 0
            compteur = True
            for caractere in information_pays(code_pays) :
                if caractere in ['0','1','2','3','4','5','6','7','8','9'] and compteur :
                    n += 1
                    compteur = False
                if caractere not in [',','.','0','1','2','3','4','5','6','7','8','9'] :
                    compteur = True
            if n > n_max :
                n_max = n

        # On considère que si le nombre de valeurs dans l'information est au plus égal à deux alors le seul problème se trouve si on demande
        # de ne pas compter les îles dans la superficie d'un pays qui paraît ne pas être logique si on veut comparer les pays correctement

        # Fonction qui compare deux informations

        def comparaison(information1, information2) :

            # Est ce que dans cette information il y a un ordre de grandeur
            ordre1 = ''
            for caractere in information1 :
                if caractere not in [',','.','0','1','2','3','4','5','6','7','8','9','$','%',' ','-'] :
                    ordre1 += caractere
            ordre2 = ''
            for caractere in information2 :
                if caractere not in [',','.','0','1','2','3','4','5','6','7','8','9','$','%',' ','-'] :
                    ordre2 += caractere

            # Si non ou qu'ils sont égaux, on compare simplement les valeurs
            if ordre1 == ordre2 :

                valeur1 = ''
                for caractere in information1 :
                    if caractere in [',','.','0','1','2','3','4','5','6','7','8','9','-'] :
                        valeur1 += caractere
                valeur1 = valeur1.replace(',','')

                valeur2 = ''
                for caractere in information2 :
                    if caractere in [',','.','0','1','2','3','4','5','6','7','8','9','-'] :
                        valeur2 += caractere
                valeur2 = valeur2.replace(',','')

                # Si la valeur de l'information 2 est plus petite on retourne 1
                if float(valeur1) > float(valeur2) :
                    return 2

            # Si les ordres sont différents alors on les compare
            else :

                # Si l'ordre du premier est du million et que les deux ordres sont différents alors ordre2 est plus grand
                if ordre1 == 'million' :
                    return 1
                elif ordre2 == 'million' :
                    return 2
                elif ordre1 == 'trillion' :
                    return 2
                elif ordre2 == 'trillion' :
                    return 1

        # Création et remplissage d'une liste contenant les codes des pays

        if n_max < 3 :

            # Liste contenant le code des pays qui nous intéressent
            liste_code_pays = []

            # Demande à l'utilisateur l'année à laquelle il veut se référer si besoin

            # Est-ce qu'il y a des pourcentages ou des sommes d'argent ?
            nb_pourcentage_max = 0
            nb_dollar_max = 0

            for indice_code_pays in range(len(self.data)) :
                info = information_pays(indice_code_pays)
                info_nb_pourcentage = info.count('%')
                info_nb_dollar = info.count('$')
                if info_nb_pourcentage > nb_pourcentage_max or info_nb_dollar > nb_dollar_max :
                    nb_pourcentage_max = info_nb_pourcentage
                    nb_dollar_max = info_nb_dollar

            annee = ''
            if nb_dollar_max == 1 or nb_pourcentage_max == 1 :

                # On affiche la liste des années disponibles
                liste_annee = []
                for code_pays in range(len(self.data)) :
                    for i in range(len(information_pays(code_pays))) :
                        if information_pays(code_pays)[i] == '(' :
                            pseudo_annee = ''
                            j = i
                            while j < len(information_pays(code_pays))-3 and pseudo_annee == '' :
                                un = information_pays(code_pays)[j]
                                deux = information_pays(code_pays)[j+1]
                                trois = information_pays(code_pays)[j+2]
                                quatre = information_pays(code_pays)[j+3]
                                annee_ou_pas = un + deux + trois + quatre
                                vrai = True
                                for chiffre in annee_ou_pas :
                                    if chiffre not in ['0','1','2','3','4','5','6','7','8','9'] :
                                        vrai = False
                                if vrai :
                                    pseudo_annee = annee_ou_pas
                                j += 1
                            if pseudo_annee != '' and pseudo_annee not in liste_annee :
                                liste_annee += [pseudo_annee]

                # On demande à l'utiliateur l'année qui l'intéresse
                print('Liste des années que vous pouvez choisir :' ,liste_annee)
                while True : 
                    annee = input('A quelle annee souhaitez vous faire reference (tapez par exemple : 2015 ou si vous souhaitez les données les plus récentes de chaque pays, tapez : recentes) ? ')
                    if annee in liste_annee or annee=='recentes': 
                        break

                # Verifions que les informations concernant cette annee sont bien presentes pour tous les pays
                if annee != 'recentes' :
                    annee_presente = True
                    for indice_code_pays in range(len(self.data)) :
                        if annee not in information_pays(indice_code_pays) :
                            annee_presente = False
                    if not annee_presente :
                        print('Le classement sera fait par rapport aux pays dont des informations liées à cette année ont été référencé')

            # Initialisation : création d'une liste contenant le code d'un pays
            code_pays = 0

            if (nb_dollar_max == 1 or nb_pourcentage_max == 1) and annee != 'recentes' :
                while liste_code_pays == [] :
                    if annee in information_pays(code_pays) :
                        liste_code_pays = [code_pays]
                    else :
                        code_pays += 1
                        if code_pays >= len(self.data) :
                            raise NameError('Les informations associées à cette année ne sont pas dans cette base de données')

            else :
                liste_code_pays = [code_pays]

            # Pays suivant

            code_pays += 1

            # Comparaison du pays avec ceux déjà dans la liste

            while code_pays < len(self.data) :

                information1 = information_pays(code_pays)
                # On va comparer cette information aux autres de la liste

                # On initialise l'indice du pays de la liste représentant la borne inférieure au pays de la base de données
                indice = -1

                for indice_code_pays_liste in range(len(liste_code_pays)) :
                    valeur1 = ''
                    information2 = information_pays(liste_code_pays[indice_code_pays_liste])
                    valeur2 = ''

                    # Si oui, on trouve les valeurs
                    if nb_pourcentage_max == 1 or nb_dollar_max == 1 :

                        if annee == 'recentes' :

                            i = 0
                            while information1[i] not in ['0','1','2','3','4','5','6','7','8','9','$','%','-'] :
                                i += 1
                            while i < len(information1) and information1[i] in [',','.','0','1','2','3','4','5','6','7','8','9','$','%','-'] :
                                valeur1 += information1[i]
                                i += 1

                            if 'million' in information1 :
                                valeur1 += ' million'
                            if 'billion' in information1 :
                                valeur1 += ' billion'
                            if 'trillion' in information1 :
                                valeur1 += ' trillion'

                            i = 0
                            while information2[i] not in ['0','1','2','3','4','5','6','7','8','9','$','%','-'] :
                                i += 1
                            while i < len(information2) and information2[i] in [',','.','0','1','2','3','4','5','6','7','8','9','$','%','-'] :
                                valeur2 += information2[i]
                                i += 1

                            if 'million' in information2 :
                                valeur1 += ' million'
                            if 'billion' in information2 :
                                valeur1 += ' billion'
                            if 'trillion' in information2 :
                                valeur1 += ' trillion'

                        else :

                            if annee in information1 :

                                i = 0
                                while information1[i] not in ['0','1','2','3','4','5','6','7','8','9','$','%','-'] :
                                    i += 1
                                while i < len(information1) and information1[i] in [',','.','0','1','2','3','4','5','6','7','8','9','$','%','-'] :
                                    valeur1 += information1[i]
                                    i += 1

                                if 'million' in information1 :
                                    valeur1 += ' million'
                                if 'billion' in information1 :
                                    valeur1 += ' billion'
                                if 'trillion' in information1 :
                                    valeur1 += ' trillion'

                                i = 0
                                while information2[i] not in ['0','1','2','3','4','5','6','7','8','9','$','%','-'] :
                                    i += 1
                                while i < len(information2) and information2[i] in [',','.','0','1','2','3','4','5','6','7','8','9','$','%','-'] :
                                    valeur2 += information2[i]
                                    i += 1

                                if 'million' in information2 :
                                    valeur1 += ' million'
                                if 'billion' in information2 :
                                    valeur1 += ' billion'
                                if 'trillion' in information2 :
                                    valeur1 += ' trillion'

                    # Sinon on trouve quand même les valeurs xD
                    else :

                        i = 0
                        while information1[i] not in ['0','1','2','3','4','5','6','7','8','9','-'] :
                            i += 1
                        while i < len(information1) and information1[i] in [',','.','0','1','2','3','4','5','6','7','8','9','-'] :
                            valeur1 += information1[i]
                            i += 1

                        if 'million' in information1 :
                            valeur1 += ' million'
                        if 'billion' in information1 :
                            valeur1 += ' billion'
                        if 'trillion' in information1 :
                            valeur1 += ' trillion'

                        i = 0
                        while information2[i] not in ['0','1','2','3','4','5','6','7','8','9','-'] :
                            i += 1
                        while i < len(information2) and information2[i] in [',','.','0','1','2','3','4','5','6','7','8','9','-'] :
                            valeur2 += information2[i]
                            i += 1

                        if 'million' in information2 :
                            valeur1 += ' million'
                        if 'billion' in information2 :
                            valeur1 += ' billion'
                        if 'trillion' in information2 :
                            valeur1 += ' trillion'

                    if valeur1 != '' :
                        valeur_comparaison = comparaison(valeur1, valeur2)
                        if valeur_comparaison == 2 :
                                    indice = indice_code_pays_liste

                

                if valeur1 != '' :

                    
                    # Initialisation : ajout des nb_pays_max premiers pays de la base de données dans la liste contenant les codes pays

                    if len(liste_code_pays) < nb_pays_max :

                        liste_code_pays.append(0)
                        if indice == -1 :
                            for i in range(1, len(liste_code_pays)) :
                                liste_code_pays[len(liste_code_pays)-i] = liste_code_pays[len(liste_code_pays)-1-i]
                            liste_code_pays[0] = code_pays
                        else :
                            i = len(liste_code_pays)-1
                            while i != indice :
                                liste_code_pays[i] = liste_code_pays[i-1]
                                i -= 1
                            liste_code_pays[indice+1] = code_pays

                    

                    
                    # Hérédité : remplacement des pays de la liste quand celle-ci est pleine

                    else :

                        if indice == 0 :
                            liste_code_pays[indice] = code_pays

                        elif indice == len(liste_code_pays)-1 :
                            for i in range(len(liste_code_pays)-1) :
                                liste_code_pays[i] = liste_code_pays[i+1]
                            liste_code_pays[len(liste_code_pays)-1] = code_pays

                        elif indice > 0 and indice < len(liste_code_pays)-1 :
                            for i in range(indice) :
                                liste_code_pays[i] = liste_code_pays[i+1]
                            liste_code_pays[indice] = code_pays

                    

                
                # On passe au pays suivant dans la base de donnée

                code_pays += 1

                

            

        elif n_max > 2 :

            # Liste contenant le code des pays qui nous intéressent
            liste_code_pays = []

            
            # Demande à l'utilisateur l'année à laquelle il veut se référer si besoin

            # Est-ce qu'il y a des pourcentages ou des sommes d'argent ?
            nb_pourcentage_max = 0
            nb_dollar_max = 0

            for indice_code_pays in range(len(self.data)) :
                info = information_pays(indice_code_pays)
                info_nb_pourcentage = info.count('%')
                info_nb_dollar = info.count('$')
                if info_nb_pourcentage > nb_pourcentage_max or info_nb_dollar > nb_dollar_max :
                    nb_pourcentage_max = info_nb_pourcentage
                    nb_dollar_max = info_nb_dollar

            annee = ''
            if nb_dollar_max > 1 or nb_pourcentage_max > 1 :

                # On affiche la liste des années disponibles
                liste_annee = []
                for code_pays in range(len(self.data)) :
                    for i in range(len(information_pays(code_pays))) :
                        if information_pays(code_pays)[i] == '(' :
                            pseudo_annee = ''
                            j = i
                            while j < len(information_pays(code_pays))-3 and pseudo_annee == '' :
                                un = information_pays(code_pays)[j]
                                deux = information_pays(code_pays)[j+1]
                                trois = information_pays(code_pays)[j+2]
                                quatre = information_pays(code_pays)[j+3]
                                annee_ou_pas = un + deux + trois + quatre
                                vrai = True
                                for chiffre in annee_ou_pas :
                                    if chiffre not in ['0','1','2','3','4','5','6','7','8','9'] :
                                        vrai = False
                                if vrai :
                                    pseudo_annee = annee_ou_pas
                                j += 1
                            if pseudo_annee != '' and pseudo_annee not in liste_annee :
                                liste_annee += [pseudo_annee]

                # On demande à l'utiliateur l'année qui l'intéresse
                print('Liste des années que vous pouvez choisir :' ,liste_annee)
                while True : 
                    annee = input('A quelle annee souhaitez vous faire reference (tapez par exemple : 2015 ou si vous souhaitez les données les plus récentes de chaque pays, tapez : recentes) ? ')
                    if annee in liste_annee or annee=='recentes': 
                        break
                # Verifions que les informations concernant cette annee sont bien presentes pour tous les pays
                if annee != 'recentes' :
                    annee_presente = True
                    for indice_code_pays in range(len(self.data)) :
                        if annee not in information_pays(indice_code_pays) :
                            annee_presente = False
                    if not annee_presente :
                        print('Le classement sera fait par rapport aux pays dont des informations liées à cette année ont été référencé')

            

            
            # Est-ce qu'il y a la répartition hommes femmes d'une classe dans l'information

            individus_ou_non = False
            if 'female' in information_pays(code_pays) :
                individus_ou_non = True

            quels_individus = 0
            if individus_ou_non :
                while True : 
                    quels_individus = input('Souhaitez-vous les pourcentages (1) de la classe ou le nombre de femmes (2) ou de hommes (3) ? (tapez 1, 2 ou 3) ')
                    if quels_individus in ['1','2','3']: 
                        break

            

            
            # Initialisation : création d'une liste contenant le code d'un pays
            code_pays = 0

            if (nb_dollar_max > 1 or nb_pourcentage_max > 1) and annee != 'recentes' :
                while liste_code_pays == [] :
                    if annee in information_pays(code_pays) :
                        liste_code_pays = [code_pays]
                    else :
                        code_pays += 1
                        if code_pays >= len(self.data) :
                            raise NameError('Les informations associées à cette année ne sont pas dans cette base de données')

            else :
                liste_code_pays = [code_pays]


            # Pays suivant

            code_pays += 1

            # Comparaison du pays avec ceux déjà dans la liste

            while code_pays < len(self.data)-1 :

                information1 = information_pays(code_pays)
                # On va comparer cette information aux autres de la liste

                # On initialise l'indice du pays de la liste représentant la borne inférieure au pays de la base de données
                indice = -1

                for indice_code_pays_liste in range(len(liste_code_pays)) :

                    valeur1 = ''

                    information2 = information_pays(liste_code_pays[indice_code_pays_liste])
                    valeur2 = ''

                    # Si oui, et qu'il n'y a qu'une seule valeur de ce type, on trouve les valeurs
                    if (nb_pourcentage_max == 1 or nb_dollar_max == 1) or annee == 'recentes' :

                        if quels_individus == '2' or quels_individus == '3' :

                            i = 0
                            while valeur1 == '' :

                                if quels_individus == '2' :
                                    f_1 = information1[i]
                                    e_1_1 = information1[i+1]
                                    m_1 = information1[i+2]
                                    a_1 = information1[i+3]
                                    l_1 = information1[i+4]
                                    e_2_1 = information1[i+5]
                                    if f_1 + e_1_1 + m_1 + a_1 + l_1 + e_2_1 == 'female' :
                                        while information1[i] not in ['0','1','2','3','4','5','6','7','8','9'] :
                                            i = i+1
                                        while information1[i] in [',','0','1','2','3','4','5','6','7','8','9'] :
                                            valeur1 += information1[i]
                                            i += 1
                                    else :
                                        i += 1

                                elif quels_individus == '3' :
                                    m_1 = information1[i]
                                    a_1 = information1[i+1]
                                    l_1 = information1[i+2]
                                    e_1 = information1[i+3]
                                    if m_1 + a_1 + l_1 + e_1 == 'male' :
                                        while information1[i] not in ['0','1','2','3','4','5','6','7','8','9'] :
                                            i = i+1
                                        while information1[i] in [',','0','1','2','3','4','5','6','7','8','9'] :
                                            valeur1 += information1[i]
                                            i += 1
                                    else :
                                        i += 1

                            j = 0
                            while valeur2 == '' :

                                if quels_individus == '2' :
                                    f_2 = information2[j]
                                    e_1_2 = information2[j+1]
                                    m_2 = information2[j+2]
                                    a_2 = information2[j+3]
                                    l_2 = information2[j+4]
                                    e_2_2 = information2[j+5]
                                    if f_2 + e_1_2 + m_2 + a_2 + l_2 + e_2_2 == 'female' :
                                        while information2[j] not in ['0','1','2','3','4','5','6','7','8','9'] :
                                            j = j+1
                                        while information2[j] in [',','0','1','2','3','4','5','6','7','8','9'] :
                                            valeur2 += information2[j]
                                            j += 1
                                    else :
                                        j += 1

                                elif quels_individus == '3' :
                                    m_2 = information2[j]
                                    a_2 = information2[j+1]
                                    l_2 = information2[j+2]
                                    e_2 = information2[j+3]
                                    if m_2 + a_2 + l_2 + e_2 == 'male' :
                                        while information2[j] not in ['0','1','2','3','4','5','6','7','8','9'] :
                                            j = j+1
                                        while information2[j] in [',','0','1','2','3','4','5','6','7','8','9'] :
                                            valeur2 += information2[j]
                                            j += 1
                                    else :
                                        j += 1

                            valeur1 = valeur1.replace(',','')
                            valeur2 = valeur2.replace(',','')

                        else :

                            i = 0
                            while information1[i] not in ['0','1','2','3','4','5','6','7','8','9','$','%','-'] :
                                i += 1
                            while i < len(information1) and information1[i] in [',','.','0','1','2','3','4','5','6','7','8','9','$','%','-'] :
                                valeur1 += information1[i]
                                i += 1

                            if 'million' in information1 :
                                valeur1 += ' million'
                            if 'billion' in information1 :
                                valeur1 += ' billion'
                            if 'trillion' in information1 :
                                valeur1 += ' trillion'

                            i = 0
                            while information2[i] not in ['0','1','2','3','4','5','6','7','8','9','$','%','-'] :
                                i += 1
                            while i < len(information2) and information2[i] in [',','.','0','1','2','3','4','5','6','7','8','9','$','%','-'] :
                                valeur2 += information2[i]
                                i += 1

                            if 'million' in information2 :
                                valeur2 += ' million'
                            if 'billion' in information2 :
                                valeur2 += ' billion'
                            if 'trillion' in information2 :
                                valeur2 += ' trillion'

                    # Sinon, on trouve aussi les valeurs xD
                    else :

                        # Condition : l'année doit être dans la première information
                        # Si elle n'y est pas on passe le pays
                        if annee in information1 :

                            # Trouvons où est écrite l'année dans les informations
                            indice_annee_1 = -1
                            for indice_annee in range(len(information1)-3) :
                                if information1[indice_annee] + information1[indice_annee+1] + information1[indice_annee+2] + information1[indice_annee+3] == annee :
                                    indice_annee_1 = indice_annee
                            indice_annee_2 = -1
                            for indice_annee in range(len(information2)-3) :
                                if information2[indice_annee] + information2[indice_annee+1] + information2[indice_annee+2] + information2[indice_annee+3] == annee :
                                    indice_annee_2 = indice_annee

                            # Trouvons où debute la paranthèse dans les informations
                            i = 0
                            while information1[indice_annee_1-i] != '(' :
                                i += 1
                            indice_paranthese_1 = indice_annee_1-i
                            i = 0
                            while information2[indice_annee_2-i] != '(' :
                                i += 1
                            indice_paranthese_2 = indice_annee_2-i

                            # Où est la valeur associée à l'information 1 et à l'année ? Quelle est elle ?

                            chercher = True
                            indice_valeur_max_1 = -1
                            for indice_valeur in range(indice_paranthese_1) :
                                if information1[indice_paranthese_1 - 1 - indice_valeur] in ['0','1','2','3','4','5','6','7','8','9','$','%'] and chercher :
                                    indice_valeur_max_1 = indice_paranthese_1 - 1 - indice_valeur
                                    chercher = False

                            i = 0
                            while indice_valeur_max_1-1-i >= 0 and  information1[indice_valeur_max_1 - 1 - i] in [',','.','0','1','2','3','4','5','6','7','8','9','$','%','-'] :
                                i += 1
                            indice_valeur_min_1 = indice_valeur_max_1-i

                            for indice_valeur in range(indice_valeur_min_1,indice_valeur_max_1+1) :
                                valeur1 += information1[indice_valeur]

                            if 'million' in information1 :
                                valeur1 += ' million'
                            if 'billion' in information1 :
                                valeur1 += ' billion'
                            if 'trillion' in information1 :
                                valeur1 += ' trillion'

                            # Où est la valeur associée à l'information 2 et à l'année ? Quelle est elle ?

                            chercher = True
                            indice_valeur_max_2 = -1
                            for indice_valeur in range(indice_paranthese_2) :
                                if information2[indice_paranthese_2 - 1 - indice_valeur] in ['0','1','2','3','4','5','6','7','8','9','$','%'] and chercher :
                                    indice_valeur_max_2 = indice_paranthese_2 - 1 - indice_valeur
                                    chercher = False

                            i = 0
                            while indice_valeur_max_2-1-i >= 0 and information2[indice_valeur_max_2 - 1 - i] in [',','.','0','1','2','3','4','5','6','7','8','9','$','%','-'] :
                                i += 1
                            indice_valeur_min_2 = indice_valeur_max_2-i

                            for indice_valeur in range(indice_valeur_min_2,indice_valeur_max_2+1) :
                                valeur2 += information2[indice_valeur]

                            if 'million' in information2 :
                                valeur2 += ' million'
                            if 'billion' in information2 :
                                valeur2 += ' billion'
                            if 'trillion' in information2 :
                                valeur2 += ' trillion'

                    if valeur1 != '' :
                        valeur_comparaison = comparaison(valeur1, valeur2)
                        if valeur_comparaison == 2 :
                            indice = indice_code_pays_liste

                

                # Est-ce que la valeur existe ?
                if valeur1 != '' :

                    
                    # Initialisation : ajout des nb_pays_max premiers pays de la base de données dans la liste contenant les codes pays

                    if len(liste_code_pays) < nb_pays_max :

                        liste_code_pays.append(0)
                        if indice == -1 :
                            for i in range(1, len(liste_code_pays)) :
                                liste_code_pays[len(liste_code_pays)-i] = liste_code_pays[len(liste_code_pays)-1-i]
                            liste_code_pays[0] = code_pays
                        else :
                            i = len(liste_code_pays)-1
                            while i != indice :
                                liste_code_pays[i] = liste_code_pays[i-1]
                                i -= 1
                            liste_code_pays[indice+1] = code_pays
                 
                    # Hérédité : remplacement des pays de la liste quand celle-ci est pleine

                    else :

                        if indice == 0 :
                            liste_code_pays[indice] = code_pays

                        elif indice == len(liste_code_pays)-1 :
                            for i in range(len(liste_code_pays)-1) :
                                liste_code_pays[i] = liste_code_pays[i+1]
                            liste_code_pays[len(liste_code_pays)-1] = code_pays

                        elif indice > 0 and indice < len(liste_code_pays)-1 :
                            for i in range(indice) :
                                liste_code_pays[i] = liste_code_pays[i+1]
                            liste_code_pays[indice] = code_pays

                # On passe au pays suivant dans la base de donnée

                code_pays += 1

        # On transforme la liste de codes en une liste de noms que l'on retourne

        liste_nom_pays = []
        for code_pays in liste_code_pays :
            liste_nom_pays += [self.data[code_pays]['Government']['Country name']['conventional short form']['text']]

        print("\nRésultats : \n")
        for code in range(len(liste_code_pays)) :
            print("• {} - {}".format(liste_nom_pays[code],information_pays(liste_code_pays[code])))

        input("\nAffichage terminé, appuyez sur Entrer pour continuer ")

    # Fonction resume d'informations, dépassement d'un seuil

    def informations_seuil_inf(self,critere):
        while True : 
            seuil = input("Entrez le seuil en pourcentage :")
            if fbd.is_number(seuil): 
                break
        # Fonction qui trouve quel est le chemin pour acceder au critere demandé

        def chemin(critere) :

            chemin_critere = []

            code_pays = 0
            while code_pays < len(self.data) and chemin_critere == [] :
                for a in self.data[code_pays] :
                    if a == critere :
                        chemin_critere = [a]
                    else :
                        if a != 'text' :
                            for b in self.data[code_pays][a] :
                                if b == critere :
                                    chemin_critere = [a,b]
                                else :
                                    if b != 'text' :
                                        for c in self.data[code_pays][a][b] :
                                            if c == critere :
                                                chemin_critere = [a,b,c]
                code_pays += 1

            return chemin_critere

        # Determination du chemin pour accéder au critere
        chemin = chemin(critere)

        # Est ce que le dernier critere est atteint ? Sinon, on le choisit :

        test_text = False
        if len(chemin) == 1 :
            for suite in self.data[0][chemin[0]] :
                if str(suite) == 'text' :
                    test_text = True
            if not test_text :
                for suite in self.data[0][chemin[0]] :
                    print(suite)
                choix_dernier_critere = input('Choisissez le critere voulu (par exemple : ecrire total et non "total") :')
                chemin += [choix_dernier_critere]

        test_text = False
        if len(chemin) == 2 :
            for suite in self.data[0][chemin[0]][chemin[1]] :
                if str(suite) == 'text' :
                    test_text = True
            if not test_text :
                for suite in self.data[0][chemin[0]][chemin[1]] :
                    print(suite)
                choix_dernier_critere = input('Choisissez le critere voulu (par exemple : ecrire total et non "total") :')
                chemin += [choix_dernier_critere]

        if chemin == [] :
            raise NameError('Critère non reconnu')
            # Critere qui n'est pas dans la base de données


        def information_pays(code_pays) :

            if len(chemin) == 1 :
                return self.data[code_pays][chemin[0]]['text']
            elif len(chemin) == 2 :
                return self.data[code_pays][chemin[0]][chemin[1]]['text']
            else :
                return self.data[code_pays][chemin[0]][chemin[1]][chemin[2]]['text']

        # L'utilisateur doit il choisir l'information qui l'intéresse ? Pour cela comptons les valeurs dans l'information

        # On comte le nombre n de valeurs dans les informations et on garde le max
        n_max = 0

        for code_pays in range(len(self.data)) :

            n = 0
            compteur = True
            for caractere in information_pays(code_pays) :
                if caractere in ['0','1','2','3','4','5','6','7','8','9'] and compteur :
                    n += 1
                    compteur = False
                if caractere not in [',','.','0','1','2','3','4','5','6','7','8','9'] :
                    compteur = True
            if n > n_max :
                n_max = n

        # On considère que si le nombre de valeurs dans l'information est au plus égal à deux alors le seul problème se trouve si on demande
        # de ne pas compter les îles dans la superficie d'un pays qui paraît ne pas être logique si on veut comparer les pays correctement

        # Fonction qui compare deux informations

        def comparaison(information1,information2) :

            # Est ce que dans cette information il y a un ordre de grandeur
            ordre1 = ''
            for caractere in information1 :
                if caractere not in [',','.','0','1','2','3','4','5','6','7','8','9','$','%',' ','-'] :
                    ordre1 += caractere
            ordre2 = ''
            for caractere in information2 :
                if caractere not in [',','.','0','1','2','3','4','5','6','7','8','9','$','%',' ','-'] :
                    ordre2 += caractere

            # Si non ou qu'ils sont égaux, on compare simplement les valeurs
            if ordre1 == ordre2 :

                valeur1 = ''
                for caractere in information1 :
                    if caractere in [',','.','0','1','2','3','4','5','6','7','8','9','-'] :
                        valeur1 += caractere
                valeur1 = valeur1.replace(',','')

                valeur2 = ''
                for caractere in information2 :
                    if caractere in [',','.','0','1','2','3','4','5','6','7','8','9','-'] :
                        valeur2 += caractere
                valeur2 = valeur2.replace(',','')

                # Si la valeur de l'information 2 est plus petite on retourne 2
                if float(valeur1) >= float(valeur2) :
                    return 2

            # Si les ordres sont différents alors on les compare
            else :

                # Si l'ordre du premier est du million et que les deux ordres sont différents alors ordre2 est plus grand
                if ordre1 == 'million' :
                    return 1
                elif ordre2 == 'million' :
                    return 2
                elif ordre1 == 'trillion' :
                    return 2
                elif ordre2 == 'trillion' :
                    return 1

        valeur_seuil = ''
        i = 0
        while seuil[i] not in ['0','1','2','3','4','5','6','7','8','9','$','%','-'] :
            i += 1
        while i < len(seuil) and seuil[i] in [',','.','0','1','2','3','4','5','6','7','8','9','$','%','-'] :
            valeur_seuil += seuil[i]
            i += 1

        if 'million' in seuil :
            valeur_seuil += ' million'
        if 'billion' in seuil :
            valeur_seuil += ' billion'
        if 'trillion' in seuil :
            valeur_seuil += ' trillion'

        # Création et remplissage d'une liste contenant les codes des pays

        if n_max < 3 :

            # Liste contenant le code des pays qui nous intéressent
            liste_code_pays = []

            # Demande à l'utilisateur l'année à laquelle il veut se référer si besoin

            # Est-ce qu'il y a des pourcentages ou des sommes d'argent ?
            nb_pourcentage_max = 0
            nb_dollar_max = 0

            for indice_code_pays in range(len(self.data)) :
                info = information_pays(indice_code_pays)
                info_nb_pourcentage = info.count('%')
                info_nb_dollar = info.count('$')
                if info_nb_pourcentage > nb_pourcentage_max or info_nb_dollar > nb_dollar_max :
                    nb_pourcentage_max = info_nb_pourcentage
                    nb_dollar_max = info_nb_dollar

            annee = ''
            if nb_dollar_max == 1 or nb_pourcentage_max == 1 :

                # On affiche la liste des années disponibles
                liste_annee = []
                for code_pays in range(len(self.data)) :
                    for i in range(len(information_pays(code_pays))) :
                        if information_pays(code_pays)[i] == '(' :
                            pseudo_annee = ''
                            j = i
                            while j < len(information_pays(code_pays))-3 and pseudo_annee == '' :
                                un = information_pays(code_pays)[j]
                                deux = information_pays(code_pays)[j+1]
                                trois = information_pays(code_pays)[j+2]
                                quatre = information_pays(code_pays)[j+3]
                                annee_ou_pas = un + deux + trois + quatre
                                vrai = True
                                for chiffre in annee_ou_pas :
                                    if chiffre not in ['0','1','2','3','4','5','6','7','8','9'] :
                                        vrai = False
                                if vrai :
                                    pseudo_annee = annee_ou_pas
                                j += 1
                            if pseudo_annee != '' and pseudo_annee not in liste_annee :
                                liste_annee += [pseudo_annee]

                # On demande à l'utiliateur l'année qui l'intéresse
                print('Liste des années que vous pouvez choisir :' ,liste_annee)
                while True : 
                    annee = input('A quelle annee souhaitez vous faire reference (tapez par exemple : 2015 ou si vous souhaitez les données les plus récentes de chaque pays, tapez : recentes) ? ')
                    if annee in liste_annee or annee=='recentes': 
                        break
                # Verifions que les informations concernant cette annee sont bien presentes pour tous les pays
                if annee != 'recentes' :
                    annee_presente = True
                    for indice_code_pays in range(len(self.data)) :
                        if annee not in information_pays(indice_code_pays) :
                            annee_presente = False
                    if not annee_presente :
                        print('Le classement sera fait par rapport aux pays dont des informations liées à cette année ont été référencé')


            code_pays = 0

            # Comparaison du pays avec le seuil

            while code_pays < len(self.data) :

                information1 = information_pays(code_pays)
                # On va comparer cette information au seuil
                valeur1 = ''

                if nb_pourcentage_max == 1 or nb_dollar_max == 1 :

                    if annee == 'recentes' :

                        i = 0
                        while information1[i] not in ['0','1','2','3','4','5','6','7','8','9','$','%','-'] :
                            i += 1
                        while i < len(information1) and information1[i] in [',','.','0','1','2','3','4','5','6','7','8','9','$','%','-'] :
                            valeur1 += information1[i]
                            i += 1

                        if 'million' in information1 :
                            valeur1 += ' million'
                        if 'billion' in information1 :
                            valeur1 += ' billion'
                        if 'trillion' in information1 :
                            valeur1 += ' trillion'

                    else :

                        if annee in information1 :

                            i = 0
                            while information1[i] not in ['0','1','2','3','4','5','6','7','8','9','$','%','-'] :
                                i += 1
                            while i < len(information1) and information1[i] in [',','.','0','1','2','3','4','5','6','7','8','9','$','%','-'] :
                                valeur1 += information1[i]
                                i += 1

                            if 'million' in information1 :
                                valeur1 += ' million'
                            if 'billion' in information1 :
                                valeur1 += ' billion'
                            if 'trillion' in information1 :
                                valeur1 += ' trillion'

                else :

                    i = 0
                    while information1[i] not in ['0','1','2','3','4','5','6','7','8','9','-'] :
                        i += 1
                    while i < len(information1) and information1[i] in [',','.','0','1','2','3','4','5','6','7','8','9','-'] :
                        valeur1 += information1[i]
                        i += 1

                    if 'million' in information1 :
                        valeur1 += ' million'
                    if 'billion' in information1 :
                        valeur1 += ' billion'
                    if 'trillion' in information1 :
                        valeur1 += ' trillion'

                if valeur1 != '' :
                    valeur_comparaison = comparaison(valeur1,valeur_seuil)
                    if valeur_comparaison == 2 :
                        liste_code_pays += [code_pays]


                code_pays += 1

        elif n_max > 2 :

            # Liste contenant le code des pays qui nous intéressent
            liste_code_pays = []

            
            # Demande à l'utilisateur l'année à laquelle il veut se référer si besoin

            # Est-ce qu'il y a des pourcentages ou des sommes d'argent ?
            nb_pourcentage_max = 0
            nb_dollar_max = 0

            for indice_code_pays in range(len(self.data)) :
                info = information_pays(indice_code_pays)
                info_nb_pourcentage = info.count('%')
                info_nb_dollar = info.count('$')
                if info_nb_pourcentage > nb_pourcentage_max or info_nb_dollar > nb_dollar_max :
                    nb_pourcentage_max = info_nb_pourcentage
                    nb_dollar_max = info_nb_dollar

            annee = ''
            if nb_dollar_max > 1 or nb_pourcentage_max > 1 :

                # On affiche la liste des années disponibles
                liste_annee = []
                for code_pays in range(len(self.data)) :
                    for i in range(len(information_pays(code_pays))) :
                        if information_pays(code_pays)[i] == '(' :
                            pseudo_annee = ''
                            j = i
                            while j < len(information_pays(code_pays))-3 and pseudo_annee == '' :
                                un = information_pays(code_pays)[j]
                                deux = information_pays(code_pays)[j+1]
                                trois = information_pays(code_pays)[j+2]
                                quatre = information_pays(code_pays)[j+3]
                                annee_ou_pas = un + deux + trois + quatre
                                vrai = True
                                for chiffre in annee_ou_pas :
                                    if chiffre not in ['0','1','2','3','4','5','6','7','8','9'] :
                                        vrai = False
                                if vrai :
                                    pseudo_annee = annee_ou_pas
                                j += 1
                            if pseudo_annee != '' and pseudo_annee not in liste_annee :
                                liste_annee += [pseudo_annee]

                # On demande à l'utiliateur l'année qui l'intéresse
                print('Liste des années que vous pouvez choisir :' ,liste_annee)
                while True : 
                    annee = input('A quelle annee souhaitez vous faire reference (tapez par exemple : 2015 ou si vous souhaitez les données les plus récentes de chaque pays, tapez : recentes) ? ')
                    if annee in liste_annee or annee=='recentes': 
                        break
                # Verifions que les informations concernant cette annee sont bien presentes pour tous les pays
                if annee != 'recentes' :
                    annee_presente = True
                    for indice_code_pays in range(len(self.data)) :
                        if annee not in information_pays(indice_code_pays) :
                            annee_presente = False
                    if not annee_presente :
                        print('Le classement sera fait par rapport aux pays dont des informations liées à cette année ont été référencé')


            # Est-ce qu'il y a la répartition hommes femmes d'une classe dans l'information

            individus_ou_non = False
            if 'female' in information_pays(code_pays) :
                individus_ou_non = True

            quels_individus = 0
            if individus_ou_non :
                while True : 
                    quels_individus = input('Souhaitez-vous les pourcentages (1) de la classe ou le nombre de femmes (2) ou de hommes (3) ? (tapez 1, 2 ou 3) ')
                    if quels_individus in ['1','2','3']: 
                        break


            code_pays = 0


            # Comparaison du pays avec ceux déjà dans la liste

            while code_pays < len(self.data)-1 :

                information1 = information_pays(code_pays)
                # On va comparer cette information au seuil
                valeur1 = ''

                # Si oui, et qu'il n'y a qu'une seule valeur de ce type, on trouve les valeurs
                if (nb_pourcentage_max == 1 or nb_dollar_max == 1) or annee == 'recentes' :

                    if quels_individus == '2' or quels_individus == '3' :

                        i = 0
                        while valeur1 == '' :

                            if quels_individus == '2' :
                                f_1 = information1[i]
                                e_1_1 = information1[i+1]
                                m_1 = information1[i+2]
                                a_1 = information1[i+3]
                                l_1 = information1[i+4]
                                e_2_1 = information1[i+5]
                                if f_1 + e_1_1 + m_1 + a_1 + l_1 + e_2_1 == 'female' :
                                    while information1[i] not in ['0','1','2','3','4','5','6','7','8','9'] :
                                        i = i+1
                                    while information1[i] in [',','0','1','2','3','4','5','6','7','8','9'] :
                                        valeur1 += information1[i]
                                        i += 1
                                else :
                                    i += 1

                            elif quels_individus == '3' :
                                m_1 = information1[i]
                                a_1 = information1[i+1]
                                l_1 = information1[i+2]
                                e_1 = information1[i+3]
                                if m_1 + a_1 + l_1 + e_1 == 'male' :
                                    while information1[i] not in ['0','1','2','3','4','5','6','7','8','9'] :
                                        i = i+1
                                    while information1[i] in [',','0','1','2','3','4','5','6','7','8','9'] :
                                        valeur1 += information1[i]
                                        i += 1
                                else :
                                    i += 1

                        valeur1 = valeur1.replace(',','')

                    else :

                        i = 0
                        while information1[i] not in ['0','1','2','3','4','5','6','7','8','9','$','%','-'] :
                            i += 1
                        while i < len(information1) and information1[i] in [',','.','0','1','2','3','4','5','6','7','8','9','$','%','-'] :
                            valeur1 += information1[i]
                            i += 1

                        if 'million' in information1 :
                            valeur1 += ' million'
                        if 'billion' in information1 :
                            valeur1 += ' billion'
                        if 'trillion' in information1 :
                            valeur1 += ' trillion'


                # Sinon, on trouve aussi les valeurs xD
                else :

                    # Condition : l'année doit être dans la première information
                    # Si elle n'y est pas on passe le pays
                    if annee in information1 :

                        # Trouvons où est écrite l'année dans l'information
                        indice_annee_1 = -1
                        for indice_annee in range(len(information1)-3) :
                            if information1[indice_annee] + information1[indice_annee+1] + information1[indice_annee+2] + information1[indice_annee+3] == annee :
                                indice_annee_1 = indice_annee

                        # Trouvons où debute la paranthèse dans l'information
                        i = 0
                        while information1[indice_annee_1-i] != '(' :
                            i += 1
                        indice_paranthese_1 = indice_annee_1-i

                        # Où est la valeur associée à l'information 1 et à l'année ? Quelle est elle ?

                        chercher = True
                        indice_valeur_max_1 = -1
                        for indice_valeur in range(indice_paranthese_1) :
                            if information1[indice_paranthese_1 - 1 - indice_valeur] in ['0','1','2','3','4','5','6','7','8','9','$','%'] and chercher :
                                indice_valeur_max_1 = indice_paranthese_1 - 1 - indice_valeur
                                chercher = False

                        i = 0
                        while indice_valeur_max_1-1-i >= 0 and  information1[indice_valeur_max_1 - 1 - i] in [',','.','0','1','2','3','4','5','6','7','8','9','$','%','-'] :
                            i += 1
                        indice_valeur_min_1 = indice_valeur_max_1-i

                        for indice_valeur in range(indice_valeur_min_1,indice_valeur_max_1+1) :
                            valeur1 += information1[indice_valeur]

                        if 'million' in information1 :
                            valeur1 += ' million'
                        if 'billion' in information1 :
                            valeur1 += ' billion'
                        if 'trillion' in information1 :
                            valeur1 += ' trillion'

                if valeur1 != '' :
                    valeur_comparaison = comparaison(valeur1, valeur_seuil)
                    if valeur_comparaison == 2 :
                        liste_code_pays += [code_pays]
                
                # On passe au pays suivant dans la base de donnée

                code_pays += 1


        # On transforme la liste de codes en une liste de noms que l'on retourne

        liste_nom_pays = []
        for code_pays in liste_code_pays :
            liste_nom_pays += [self.data[code_pays]['Government']['Country name']['conventional short form']['text']]

        print("\nRésultats : \n")
        for code in range(len(liste_code_pays)) :
            print("• {} - {}".format(liste_nom_pays[code],information_pays(liste_code_pays[code])))

        input("\nAffichage terminé, appuyez sur Entrer pour continuer ")


    # Fonction resume d'informations, non dépassement d'un seuil

    def informations_seuil_supp(self,critere):

        while True : 
            seuil = input("Entrez le seuil en pourcentage :")
            if fbd.is_number(seuil): 
                break
        # Fonction qui trouve quel est le chemin pour acceder au critere demandé

        def chemin(critere) :

            chemin_critere = []

            code_pays = 0
            while code_pays < len(self.data) and chemin_critere == [] :
                for a in self.data[code_pays] :
                    if a == critere :
                        chemin_critere = [a]
                    else :
                        if a != 'text' :
                            for b in self.data[code_pays][a] :
                                if b == critere :
                                    chemin_critere = [a,b]
                                else :
                                    if b != 'text' :
                                        for c in self.data[code_pays][a][b] :
                                            if c == critere :
                                                chemin_critere = [a,b,c]
                code_pays += 1

            return chemin_critere

        

        
        # Determination du chemin pour accéder au critere
        chemin = chemin(critere)

        # Est ce que le dernier critere est atteint ? Sinon, on le choisit :

        test_text = False
        if len(chemin) == 1 :
            for suite in self.data[0][chemin[0]] :
                if str(suite) == 'text' :
                    test_text = True
            if not test_text :
                for suite in self.data[0][chemin[0]] :
                    print(suite)
                choix_dernier_critere = input('Choisissez le critere voulu (par exemple : ecrire total et non "total") :')
                chemin += [choix_dernier_critere]

        test_text = False
        if len(chemin) == 2 :
            for suite in self.data[0][chemin[0]][chemin[1]] :
                if str(suite) == 'text' :
                    test_text = True
            if not test_text :
                for suite in self.data[0][chemin[0]][chemin[1]] :
                    print(suite)
                choix_dernier_critere = input('Choisissez le critere voulu (par exemple : ecrire total et non "total") :')
                chemin += [choix_dernier_critere]

        if chemin == [] :
            raise NameError('Critère non reconnu')
            # Critere qui n'est pas dans la base de données

        
        # Fonction qui donne l'information associée à un critere et à un pays

        def information_pays(code_pays) :

            if len(chemin) == 1 :
                return self.data[code_pays][chemin[0]]['text']
            elif len(chemin) == 2 :
                return self.data[code_pays][chemin[0]][chemin[1]]['text']
            else :
                return self.data[code_pays][chemin[0]][chemin[1]][chemin[2]]['text']

        

        # L'utilisateur doit il choisir l'information qui l'intéresse ? Pour cela comptons les valeurs dans l'information

        # On comte le nombre n de valeurs dans les informations et on garde le max
        n_max = 0

        for code_pays in range(len(self.data)) :

            n = 0
            compteur = True
            for caractere in information_pays(code_pays) :
                if caractere in ['0','1','2','3','4','5','6','7','8','9'] and compteur :
                    n += 1
                    compteur = False
                if caractere not in [',','.','0','1','2','3','4','5','6','7','8','9'] :
                    compteur = True
            if n > n_max :
                n_max = n

        # On considère que si le nombre de valeurs dans l'information est au plus égal à deux alors le seul problème se trouve si on demande
        # de ne pas compter les îles dans la superficie d'un pays qui paraît ne pas être logique si on veut comparer les pays correctement

        
        # Fonction qui compare deux informations

        def comparaison(information1,information2) :

            # Est ce que dans cette information il y a un ordre de grandeur
            ordre1 = ''
            for caractere in information1 :
                if caractere not in [',','.','0','1','2','3','4','5','6','7','8','9','$','%',' ','-'] :
                    ordre1 += caractere
            ordre2 = ''
            for caractere in information2 :
                if caractere not in [',','.','0','1','2','3','4','5','6','7','8','9','$','%',' ','-'] :
                    ordre2 += caractere

            # Si non ou qu'ils sont égaux, on compare simplement les valeurs
            if ordre1 == ordre2 :

                valeur1 = ''
                for caractere in information1 :
                    if caractere in [',','.','0','1','2','3','4','5','6','7','8','9','-'] :
                        valeur1 += caractere
                valeur1 = valeur1.replace(',','')

                valeur2 = ''
                for caractere in information2 :
                    if caractere in [',','.','0','1','2','3','4','5','6','7','8','9','-'] :
                        valeur2 += caractere
                valeur2 = valeur2.replace(',','')

                # Si la valeur de l'information 2 est plus petite on retourne 2
                if float(valeur1) <= float(valeur2) :
                    return 1

            # Si les ordres sont différents alors on les compare
            else :

                # Si l'ordre du premier est du million et que les deux ordres sont différents alors ordre2 est plus grand
                if ordre1 == 'million' :
                    return 1
                elif ordre2 == 'million' :
                    return 2
                elif ordre1 == 'trillion' :
                    return 2
                elif ordre2 == 'trillion' :
                    return 1

        

        valeur_seuil = ''
        i = 0
        while seuil[i] not in ['0','1','2','3','4','5','6','7','8','9','$','%','-'] :
            i += 1
        while i < len(seuil) and seuil[i] in [',','.','0','1','2','3','4','5','6','7','8','9','$','%','-'] :
            valeur_seuil += seuil[i]
            i += 1

        if 'million' in seuil :
            valeur_seuil += ' million'
        if 'billion' in seuil :
            valeur_seuil += ' billion'
        if 'trillion' in seuil :
            valeur_seuil += ' trillion'

        
        # Création et remplissage d'une liste contenant les codes des pays

        if n_max < 3 :

            # Liste contenant le code des pays qui nous intéressent
            liste_code_pays = []

            
            # Demande à l'utilisateur l'année à laquelle il veut se référer si besoin

            # Est-ce qu'il y a des pourcentages ou des sommes d'argent ?
            nb_pourcentage_max = 0
            nb_dollar_max = 0

            for indice_code_pays in range(len(self.data)) :
                info = information_pays(indice_code_pays)
                info_nb_pourcentage = info.count('%')
                info_nb_dollar = info.count('$')
                if info_nb_pourcentage > nb_pourcentage_max or info_nb_dollar > nb_dollar_max :
                    nb_pourcentage_max = info_nb_pourcentage
                    nb_dollar_max = info_nb_dollar

            annee = ''
            if nb_dollar_max == 1 or nb_pourcentage_max == 1 :

                # On affiche la liste des années disponibles
                liste_annee = []
                for code_pays in range(len(self.data)) :
                    for i in range(len(information_pays(code_pays))) :
                        if information_pays(code_pays)[i] == '(' :
                            pseudo_annee = ''
                            j = i
                            while j < len(information_pays(code_pays))-3 and pseudo_annee == '' :
                                un = information_pays(code_pays)[j]
                                deux = information_pays(code_pays)[j+1]
                                trois = information_pays(code_pays)[j+2]
                                quatre = information_pays(code_pays)[j+3]
                                annee_ou_pas = un + deux + trois + quatre
                                vrai = True
                                for chiffre in annee_ou_pas :
                                    if chiffre not in ['0','1','2','3','4','5','6','7','8','9'] :
                                        vrai = False
                                if vrai :
                                    pseudo_annee = annee_ou_pas
                                j += 1
                            if pseudo_annee != '' and pseudo_annee not in liste_annee :
                                liste_annee += [pseudo_annee]

                # On demande à l'utiliateur l'année qui l'intéresse
                print('Liste des années que vous pouvez choisir :' ,liste_annee)
                while True : 
                    annee = input('A quelle annee souhaitez vous faire reference (tapez par exemple : 2015 ou si vous souhaitez les données les plus récentes de chaque pays, tapez : recentes) ? ')
                    if annee in liste_annee or annee=='recentes': 
                        break

                # Verifions que les informations concernant cette annee sont bien presentes pour tous les pays
                if annee != 'recentes' :
                    annee_presente = True
                    for indice_code_pays in range(len(self.data)) :
                        if annee not in information_pays(indice_code_pays) :
                            annee_presente = False
                    if not annee_presente :
                        print('Le classement sera fait par rapport aux pays dont des informations liées à cette année ont été référencé')


            code_pays = 0
      # Comparaison du pays avec le seuil

            while code_pays < len(self.data) :

                information1 = information_pays(code_pays)
                # On va comparer cette information au seuil
                valeur1 = ''

                if nb_pourcentage_max == 1 or nb_dollar_max == 1 :

                    if annee == 'recentes' :

                        i = 0
                        while information1[i] not in ['0','1','2','3','4','5','6','7','8','9','$','%','-'] :
                            i += 1
                        while i < len(information1) and information1[i] in [',','.','0','1','2','3','4','5','6','7','8','9','$','%','-'] :
                            valeur1 += information1[i]
                            i += 1

                        if 'million' in information1 :
                            valeur1 += ' million'
                        if 'billion' in information1 :
                            valeur1 += ' billion'
                        if 'trillion' in information1 :
                            valeur1 += ' trillion'

                    else :

                        if annee in information1 :

                            i = 0
                            while information1[i] not in ['0','1','2','3','4','5','6','7','8','9','$','%','-'] :
                                i += 1
                            while i < len(information1) and information1[i] in [',','.','0','1','2','3','4','5','6','7','8','9','$','%','-'] :
                                valeur1 += information1[i]
                                i += 1

                            if 'million' in information1 :
                                valeur1 += ' million'
                            if 'billion' in information1 :
                                valeur1 += ' billion'
                            if 'trillion' in information1 :
                                valeur1 += ' trillion'

                else :

                    i = 0
                    while information1[i] not in ['0','1','2','3','4','5','6','7','8','9','-'] :
                        i += 1
                    while i < len(information1) and information1[i] in [',','.','0','1','2','3','4','5','6','7','8','9','-'] :
                        valeur1 += information1[i]
                        i += 1

                    if 'million' in information1 :
                        valeur1 += ' million'
                    if 'billion' in information1 :
                        valeur1 += ' billion'
                    if 'trillion' in information1 :
                        valeur1 += ' trillion'

                if valeur1 != '' :
                    valeur_comparaison = comparaison(valeur1,valeur_seuil)
                    if valeur_comparaison == 1 :
                        liste_code_pays += [code_pays]
    
                # On passe au pays suivant dans la base de donnée

                code_pays += 1


        elif n_max > 2 :

            # Liste contenant le code des pays qui nous intéressent
            liste_code_pays = []

            
            # Demande à l'utilisateur l'année à laquelle il veut se référer si besoin

            # Est-ce qu'il y a des pourcentages ou des sommes d'argent ?
            nb_pourcentage_max = 0
            nb_dollar_max = 0

            for indice_code_pays in range(len(self.data)) :
                info = information_pays(indice_code_pays)
                info_nb_pourcentage = info.count('%')
                info_nb_dollar = info.count('$')
                if info_nb_pourcentage > nb_pourcentage_max or info_nb_dollar > nb_dollar_max :
                    nb_pourcentage_max = info_nb_pourcentage
                    nb_dollar_max = info_nb_dollar

            annee = ''
            if nb_dollar_max > 1 or nb_pourcentage_max > 1 :

                # On affiche la liste des années disponibles
                liste_annee = []
                for code_pays in range(len(self.data)) :
                    for i in range(len(information_pays(code_pays))) :
                        if information_pays(code_pays)[i] == '(' :
                            pseudo_annee = ''
                            j = i
                            while j < len(information_pays(code_pays))-3 and pseudo_annee == '' :
                                un = information_pays(code_pays)[j]
                                deux = information_pays(code_pays)[j+1]
                                trois = information_pays(code_pays)[j+2]
                                quatre = information_pays(code_pays)[j+3]
                                annee_ou_pas = un + deux + trois + quatre
                                vrai = True
                                for chiffre in annee_ou_pas :
                                    if chiffre not in ['0','1','2','3','4','5','6','7','8','9'] :
                                        vrai = False
                                if vrai :
                                    pseudo_annee = annee_ou_pas
                                j += 1
                            if pseudo_annee != '' and pseudo_annee not in liste_annee :
                                liste_annee += [pseudo_annee]

                # On demande à l'utiliateur l'année qui l'intéresse
                print('Liste des années que vous pouvez choisir :' ,liste_annee)
                while True : 
                    annee = input('A quelle annee souhaitez vous faire reference (tapez par exemple : 2015 ou si vous souhaitez les données les plus récentes de chaque pays, tapez : recentes) ? ')
                    if annee in liste_annee or annee=='recentes': 
                        break

                # Verifions que les informations concernant cette annee sont bien presentes pour tous les pays
                if annee != 'recentes' :
                    annee_presente = True
                    for indice_code_pays in range(len(self.data)) :
                        if annee not in information_pays(indice_code_pays) :
                            annee_presente = False
                    if not annee_presente :
                        print('Le classement sera fait par rapport aux pays dont des informations liées à cette année ont été référencé')

            # Est-ce qu'il y a la répartition hommes femmes d'une classe dans l'information

            individus_ou_non = False
            if 'female' in information_pays(code_pays) :
                individus_ou_non = True

            quels_individus = 0
            if individus_ou_non :
                while True : 
                    quels_individus = input('Souhaitez-vous les pourcentages (1) de la classe ou le nombre de femmes (2) ou de hommes (3) ? (tapez 1, 2 ou 3) ')
                    if quels_individus in ['1','2','3']: 
                        break


            code_pays = 0

            # Comparaison du pays avec ceux déjà dans la liste

            while code_pays < len(self.data)-1 :

                information1 = information_pays(code_pays)
                # On va comparer cette information au seuil
                valeur1 = ''

                # Si oui, et qu'il n'y a qu'une seule valeur de ce type, on trouve les valeurs
                if (nb_pourcentage_max == 1 or nb_dollar_max == 1) or annee == 'recentes' :

                    if quels_individus == '2' or quels_individus == '3' :

                        i = 0
                        while valeur1 == '' :

                            if quels_individus == '2' :
                                f_1 = information1[i]
                                e_1_1 = information1[i+1]
                                m_1 = information1[i+2]
                                a_1 = information1[i+3]
                                l_1 = information1[i+4]
                                e_2_1 = information1[i+5]
                                if f_1 + e_1_1 + m_1 + a_1 + l_1 + e_2_1 == 'female' :
                                    while information1[i] not in ['0','1','2','3','4','5','6','7','8','9'] :
                                        i = i+1
                                    while information1[i] in [',','0','1','2','3','4','5','6','7','8','9'] :
                                        valeur1 += information1[i]
                                        i += 1
                                else :
                                    i += 1

                            elif quels_individus == '3' :
                                m_1 = information1[i]
                                a_1 = information1[i+1]
                                l_1 = information1[i+2]
                                e_1 = information1[i+3]
                                if m_1 + a_1 + l_1 + e_1 == 'male' :
                                    while information1[i] not in ['0','1','2','3','4','5','6','7','8','9'] :
                                        i = i+1
                                    while information1[i] in [',','0','1','2','3','4','5','6','7','8','9'] :
                                        valeur1 += information1[i]
                                        i += 1
                                else :
                                    i += 1

                        valeur1 = valeur1.replace(',','')

                    else :

                        i = 0
                        while information1[i] not in ['0','1','2','3','4','5','6','7','8','9','$','%','-'] :
                            i += 1
                        while i < len(information1) and information1[i] in [',','.','0','1','2','3','4','5','6','7','8','9','$','%','-'] :
                            valeur1 += information1[i]
                            i += 1

                        if 'million' in information1 :
                            valeur1 += ' million'
                        if 'billion' in information1 :
                            valeur1 += ' billion'
                        if 'trillion' in information1 :
                            valeur1 += ' trillion'


                # Sinon, on trouve aussi les valeurs xD
                else :

                    # Condition : l'année doit être dans la première information
                    # Si elle n'y est pas on passe le pays
                    if annee in information1 :

                        # Trouvons où est écrite l'année dans l'information
                        indice_annee_1 = -1
                        for indice_annee in range(len(information1)-3) :
                            if information1[indice_annee] + information1[indice_annee+1] + information1[indice_annee+2] + information1[indice_annee+3] == annee :
                                indice_annee_1 = indice_annee

                        # Trouvons où debute la paranthèse dans l'information
                        i = 0
                        while information1[indice_annee_1-i] != '(' :
                            i += 1
                        indice_paranthese_1 = indice_annee_1-i

                        # Où est la valeur associée à l'information 1 et à l'année ? Quelle est elle ?

                        chercher = True
                        indice_valeur_max_1 = -1
                        for indice_valeur in range(indice_paranthese_1) :
                            if information1[indice_paranthese_1 - 1 - indice_valeur] in ['0','1','2','3','4','5','6','7','8','9','$','%'] and chercher :
                                indice_valeur_max_1 = indice_paranthese_1 - 1 - indice_valeur
                                chercher = False

                        i = 0
                        while indice_valeur_max_1-1-i >= 0 and  information1[indice_valeur_max_1 - 1 - i] in [',','.','0','1','2','3','4','5','6','7','8','9','$','%','-'] :
                            i += 1
                        indice_valeur_min_1 = indice_valeur_max_1-i

                        for indice_valeur in range(indice_valeur_min_1,indice_valeur_max_1+1) :
                            valeur1 += information1[indice_valeur]

                        if 'million' in information1 :
                            valeur1 += ' million'
                        if 'billion' in information1 :
                            valeur1 += ' billion'
                        if 'trillion' in information1 :
                            valeur1 += ' trillion'

                if valeur1 != '' :
                    valeur_comparaison = comparaison(valeur1,valeur_seuil)
                    if valeur_comparaison == 1 :
                        liste_code_pays += [code_pays]
                
                # On passe au pays suivant dans la base de donnée

                code_pays += 1
  
        # On transforme la liste de codes en une liste de noms que l'on retourne

        liste_nom_pays = []
        for code_pays in liste_code_pays :
            liste_nom_pays += [self.data[code_pays]['Government']['Country name']['conventional short form']['text']]

        print("\nRésultats : \n")
        for code in range(len(liste_code_pays)) :
            print("• {} - {}".format(liste_nom_pays[code],information_pays(liste_code_pays[code])))

        input("\nAffichage terminé, appuyez sur Entrer pour continuer ")


    # Le tableau des classes d’âge pour certains pays


    def tableau_classe_age(self):
        while True : 
            nb_pays_max = input('Combien de pays voulez vous dans le tableau ? ')
            if fbd.is_number(nb_pays_max): 
                break
        print('Vous allez rentrer le code ou le nom de' + ' nb_pays_max ')

        nom_pays = []
        classe_0_14 = []
        classe_15_24 = []
        classe_25_54 = []
        classe_55_64 = []
        classe_plus_65 = []

        for i in range(nb_pays_max) :

            code_pays = input('Rentrez un code ou un index de pays : ')

            try :
                code_pays = int(code_pays)
            except ValueError:
                for indice_code_pays in range(len(self.data)) :
                    if self.data[indice_code_pays]['Government']['Country name']['conventional short form']['text'] == code_pays :
                        code_pays = indice_code_pays
                        break

            inf1 = self.data[code_pays]['Government']['Country name']['conventional short form']['text']
            inf2 = self.data[code_pays]['People and Society']['Age structure']['0-14 years']['text']
            inf3 = self.data[code_pays]['People and Society']['Age structure']['15-24 years']['text']
            inf4 = self.data[code_pays]['People and Society']['Age structure']['25-54 years']['text']
            inf5 = self.data[code_pays]['People and Society']['Age structure']['55-64 years']['text']
            inf6 = self.data[code_pays]['People and Society']['Age structure']['65 years and over']['text']

            nom_pays += [inf1[:inf1.find(' ')]]
            classe_0_14 += [inf2[:inf2.find(' ')]]
            classe_15_24 += [inf3[:inf3.find(' ')]]
            classe_25_54 += [inf4[:inf4.find(' ')]]
            classe_55_64 += [inf5[:inf5.find(' ')]]
            classe_plus_65 += [inf6[:inf6.find(' ')]]

        Data = {'Nom du pays' : nom_pays,
                'Classe des 0-14 ans' : classe_0_14,
                'Classe des 15-24 ans' : classe_15_24,
                'Classe des 25-54 ans' : classe_25_54,
                'Classe des 55-64 ans' : classe_55_64,
                'Classe des 65 ans et plus' : classe_plus_65}

        tableau = pd.DataFrame(Data,columns=('Nom du pays',
                                            'Classe des 0-14 ans',
                                            'Classe des 15-24 ans',
                                            'Classe des 25-54 ans',
                                            'Classe des 55-64 ans',
                                            'Classe des 65 ans et plus'))

        print(tableau)





















