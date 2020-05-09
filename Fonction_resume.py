# Importation des donnees

import json
from Menus.menu_ouvert import Ouvert

# Fonction resume

def resume_information(critere):
    nb_pays_max = input("Entrez le nombre de pays max : ")
    nb_pays_max = int(nb_pays_max)
    with open("DataTreatment/country.json") as json_file:
        data = json.load(json_file)

    #------------------------------------------------------------------------------
    # Fonction qui trouve quel est le chemin pour acceder au critere demandé

    def chemin(critere) :

        chemin_critere = []

        code_pays = 0
        while code_pays < len(data) and chemin_critere == [] :
            for a in data[code_pays] :
                if a == critere :
                    chemin_critere = [a]
                else :
                    if a != 'text' :
                        for b in data[code_pays][a] :
                            if b == critere :
                                chemin_critere = [a,b]
                            else :
                                if b != 'text' :
                                    for c in data[code_pays][a][b] :
                                        if c == critere :
                                            chemin_critere = [a,b,c]
            code_pays += 1

        return chemin_critere

    #------------------------------------------------------------------------------

    #------------------------------------------------------------------------------
    # Determination du chemin pour accéder au critere
    chemin = chemin(critere)

    # Est ce que le dernier critere est atteint ? Sinon, on le choisit :

    test_text = False
    if len(chemin) == 1 :
        for suite in data[0][chemin[0]] :
            if str(suite) == 'text' :
                test_text = True
        if not test_text :
            for suite in data[0][chemin[0]] :
                print(suite)
            choix_dernier_critere = input('Choisissez le dernier critere (par exemple : ecrire total et non "total") :')
            chemin += [choix_dernier_critere]

    test_text = False
    if len(chemin) == 2 :
        for suite in data[0][chemin[0]][chemin[1]] :
            if str(suite) == 'text' :
                test_text = True
        if not test_text :
            for suite in data[0][chemin[0]][chemin[1]] :
                print(suite)
            choix_dernier_critere = input('Choisissez le dernier critere (par exemple : ecrire total et non "total") :')
            chemin += [choix_dernier_critere]

    if chemin == [] :
        raise NameError('Critère non reconnu')
        # Critere qui n'est pas dans la base de données

    if nb_pays_max > 10:
        raise NameError('Nombre de pays demandés trop élevé')
        # Erreur car nombre de pays demandés trop élevé

    #------------------------------------------------------------------------------

    #------------------------------------------------------------------------------
    # Fonction qui donne l'information associée à un critere et à un pays

    def information_pays(code_pays) :

        if len(chemin) == 1 :
            return data[code_pays][chemin[0]]['text']
        elif len(chemin) == 2 :
            return data[code_pays][chemin[0]][chemin[1]]['text']
        else :
            return data[code_pays][chemin[0]][chemin[1]][chemin[2]]['text']

    #------------------------------------------------------------------------------

    # L'utilisateur doit il choisir l'information qui l'intéresse ? Pour cela comptons les valeurs dans l'information
    # On choisit un pays aleatoirement
    import random
    code_pays_aleatoire = random.randint(0,len(data)-1)

    # On comte le nombre n de valeurs dans l'information
    n = 0

    compteur = True
    for caractere in information_pays(code_pays_aleatoire) :
        if caractere in ['0','1','2','3','4','5','6','7','8','9'] and compteur :
            n += 1
            compteur = False
        if caractere not in [',','.','0','1','2','3','4','5','6','7','8','9'] :
            compteur = True

    # On considère que si le nombre de valeurs dans l'information est au plus égal à deux alors le seul problème se trouve si on demande
    # de ne pas compter les îles dans la superficie d'un pays qui paraît ne pas être logique si on veut comparer les pays correctement

    #------------------------------------------------------------------------------
    # Fonction qui compare deux informations

    def comparaison(information1, information2) :

        # Est ce que dans cette information il y a un ordre de grandeur
        ordre1 = ''
        for caractere in information1 :
            if caractere not in [',','.','0','1','2','3','4','5','6','7','8','9','$','%',' '] :
                ordre1 += caractere
        ordre2 = ''
        for caractere in information2 :
            if caractere not in [',','.','0','1','2','3','4','5','6','7','8','9','$','%',' '] :
                ordre2 += caractere

        # Si non ou qu'ils sont égaux, on compare simplement les valeurs
        if ordre1 == ordre2 :

            valeur1 = ''
            for caractere in information1 :
                if caractere in [',','.','0','1','2','3','4','5','6','7','8','9'] :
                    valeur1 += caractere
            valeur1 = valeur1.replace(',','')

            valeur2 = ''
            for caractere in information2 :
                if caractere in [',','.','0','1','2','3','4','5','6','7','8','9'] :
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

    #------------------------------------------------------------------------------

    #------------------------------------------------------------------------------
    # Création et remplissage d'une liste contenant les codes des pays

    if n < 3 :

        #------------------------------------------------------------------------------
        # Initialisation : création d'une liste contenant le code du premier pays

        liste_code_pays = [0]

        #------------------------------------------------------------------------------

        #------------------------------------------------------------------------------
        # Choix du pays

        code_pays = 1

        #------------------------------------------------------------------------------

        #------------------------------------------------------------------------------
        # Comparaison du pays avec ceux déjà dans la liste

        while code_pays < len(data) :

            information1 = information_pays(code_pays)
            # On va comparer cette information aux autres de la liste

            # On initialise l'indice du pays de la liste représentant la borne inférieure au pays de la base de données
            indice = -1

            for indice_code_pays_liste in range(len(liste_code_pays)) :
                information2 = information_pays(liste_code_pays[indice_code_pays_liste])

                # Est-ce qu'il s'agit de pourcentages ou d'argent ?
                nb_pourcentage = 0
                nb_dollar = 0
                for caractere in information1 :
                    if caractere == '%' :
                        nb_pourcentage += 1
                    if caractere == '$' :
                        nb_dollar += 1

                # Si oui, on trouve les valeurs
                if nb_pourcentage == 1 or nb_dollar == 1 :

                    valeur1 = ''
                    i = 0
                    while information1[i] not in ['0','1','2','3','4','5','6','7','8','9','$','%'] :
                        i += 1
                    while i < len(information1) and information1[i] in [',','.','0','1','2','3','4','5','6','7','8','9','$','%'] :
                        valeur1 += information1[i]
                        i += 1

                    if 'million' in information1 :
                        valeur1 += ' million'
                    if 'billion' in information1 :
                        valeur1 += ' billion'
                    if 'trillion' in information1 :
                        valeur1 += ' trillion'

                    valeur2 = ''
                    i = 0
                    while information2[i] not in ['0','1','2','3','4','5','6','7','8','9','$','%'] :
                        i += 1
                    while i < len(information2) and information2[i] in [',','.','0','1','2','3','4','5','6','7','8','9','$','%'] :
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

                    valeur1 = ''
                    i = 0
                    while information1[i] not in ['0','1','2','3','4','5','6','7','8','9'] :
                        i += 1
                    while i < len(information1) and information1[i] in [',','.','0','1','2','3','4','5','6','7','8','9'] :
                        valeur1 += information1[i]
                        i += 1

                    if 'million' in information1 :
                        valeur1 += ' million'
                    if 'billion' in information1 :
                        valeur1 += ' billion'
                    if 'trillion' in information1 :
                        valeur1 += ' trillion'

                    valeur2 = ''
                    i = 0
                    while information2[i] not in ['0','1','2','3','4','5','6','7','8','9'] :
                        i += 1
                    while i < len(information2) and information2[i] in [',','.','0','1','2','3','4','5','6','7','8','9'] :
                        valeur2 += information2[i]
                        i += 1

                    if 'million' in information2 :
                        valeur1 += ' million'
                    if 'billion' in information2 :
                        valeur1 += ' billion'
                    if 'trillion' in information2 :
                        valeur1 += ' trillion'

                valeur_comparaison = comparaison(valeur1, valeur2)
                if valeur_comparaison == 2 :
                            indice = indice_code_pays_liste

            #------------------------------------------------------------------------------

            #------------------------------------------------------------------------------
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

            #------------------------------------------------------------------------------

            #------------------------------------------------------------------------------
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

            #------------------------------------------------------------------------------

            #------------------------------------------------------------------------------
            # On passe au pays suivant dans la base de donnée

            code_pays += 1

            #------------------------------------------------------------------------------

        #------------------------------------------------------------------------------

    if n > 2 :

        #------------------------------------------------------------------------------
        # On demande à l'utiliateur l'année qui l'intéresse

        print(information_pays(code_pays_aleatoire))
        annee = input('A quelle annee souhaitez vous faire reference ? Si on ne peut faire reference à aucune année, ne mettez rien :')

        # Verifions que les informations concernant cette annee sont bien presentes pour tous les pays
        for indice_code_pays in range(len(data)) :
            if 'annee' not in information_pays(indice_code_pays) :
                raise NameError('Les informations concernant cette annee ne sont pas disponibles pour tous les pays')

        #------------------------------------------------------------------------------

        #------------------------------------------------------------------------------
        # Initialisation : création d'une liste contenant le code du premier pays

        liste_code_pays = [0]

        #------------------------------------------------------------------------------

        #------------------------------------------------------------------------------
        # Choix du pays

        code_pays = 1

        #------------------------------------------------------------------------------

        #------------------------------------------------------------------------------
        # Comparaison du pays avec ceux déjà dans la liste

        while code_pays < len(data)-1 :

            information1 = information_pays(code_pays)
            # On va comparer cette information aux autres de la liste

            # On initialise l'indice du pays de la liste représentant la borne inférieure au pays de la base de données
            indice = -1

            for indice_code_pays_liste in range(len(liste_code_pays)) :
                information2 = information_pays(liste_code_pays[indice_code_pays_liste])

                # Est-ce qu'il s'agit de pourcentages ou d'argent ?
                nb_pourcentage = 0
                nb_dollar = 0
                for caractere in information1 :
                    if caractere == '%' :
                        nb_pourcentage += 1
                    if caractere == '$' :
                        nb_dollar += 1

                # Si oui, et qu'il n'y a qu'une seule valeur de ce type, on trouve les valeurs
                if nb_pourcentage == 1 or nb_dollar == 1 :

                    valeur1 = ''
                    i = 0
                    while information1[i] not in ['0','1','2','3','4','5','6','7','8','9','$','%'] :
                        i += 1
                    while i < len(information1) and information1[i] in [',','.','0','1','2','3','4','5','6','7','8','9','$','%'] :
                        valeur1 += information1[i]
                        i += 1

                    if 'million' in information1 :
                        valeur1 += ' million'
                    if 'billion' in information1 :
                        valeur1 += ' billion'
                    if 'trillion' in information1 :
                        valeur1 += ' trillion'

                    valeur2 = ''
                    i = 0
                    while information2[i] not in ['0','1','2','3','4','5','6','7','8','9','$','%'] :
                        i += 1
                    while i < len(information2) and information2[i] in [',','.','0','1','2','3','4','5','6','7','8','9','$','%'] :
                        valeur2 += information2[i]
                        i += 1

                    if 'million' in information2 :
                        valeur1 += ' million'
                    if 'billion' in information2 :
                        valeur1 += ' billion'
                    if 'trillion' in information2 :
                        valeur1 += ' trillion'

                # Sinon, on trouve aussi les valeurs xD
                else :

                    # Trouvons où est écrite l'année dans les informations
                    indice_annee_1 = -1
                    for indice_annee in range(len(information1)-3) :
                        if information1[indice_annee] + information1[indice_annee+1] + information1[indice_annee+2] + information1[indice_annee+3] == str(annee) :
                            indice_annee_1 = indice_annee
                    indice_annee_2 = -1
                    for indice_annee in range(len(information2)-3) :
                        if information2[indice_annee] + information2[indice_annee+1] + information2[indice_annee+2] + information2[indice_annee+3] == str(annee) :
                            indice_annee_2 = indice_annee

                    # Où est la valeur associée à l'information 1 et à l'année ? Quelle est elle ?
                    valeur1 = ''

                    chercher = True
                    indice_valeur_max_1 = -1
                    for indice_valeur in range(indice_annee_1) :
                        if information1[indice_annee_1 - 1 - indice_valeur] in ['0','1','2','3','4','5','6','7','8','9','$','%'] and chercher :
                            indice_valeur_max_1 = indice_annee_1 - 1 - indice_valeur
                            chercher = False

                    i = 0
                    while indice_valeur_max_1-1-i >= 0 and  information1[indice_valeur_max_1 - 1 - i] in [',','.','0','1','2','3','4','5','6','7','8','9','$','%'] :
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
                    valeur2 = ''

                    chercher = True
                    indice_valeur_max_2 = -1
                    for indice_valeur in range(indice_annee_2) :
                        if information2[indice_annee_2 - 1 - indice_valeur] in ['0','1','2','3','4','5','6','7','8','9','$','%'] and chercher :
                            indice_valeur_max_2 = indice_annee_2 - 1 - indice_valeur
                            chercher = False

                    i = 0
                    while indice_valeur_max_2-1-i >= 0 and information2[indice_valeur_max_2 - 1 - i] in [',','.','0','1','2','3','4','5','6','7','8','9','$','%'] :
                        i += 1
                    indice_valeur_min_2 = indice_valeur_max_2-i

                    for indice_valeur in range(indice_valeur_min_2,indice_valeur_max_2+1) :
                        valeur2 += information2[indice_valeur]

                    if 'million' in information2 :
                        valeur1 += ' million'
                    if 'billion' in information2 :
                        valeur1 += ' billion'
                    if 'trillion' in information2 :
                        valeur1 += ' trillion'

                valeur_comparaison = comparaison(valeur1, valeur2)
                if valeur_comparaison == 2 :
                    indice = indice_code_pays_liste

            #------------------------------------------------------------------------------

            #------------------------------------------------------------------------------
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

            #------------------------------------------------------------------------------

            #------------------------------------------------------------------------------
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

            #------------------------------------------------------------------------------

            #------------------------------------------------------------------------------
            # On passe au pays suivant dans la base de donnée

            code_pays += 1

            #------------------------------------------------------------------------------

        #------------------------------------------------------------------------------

    #------------------------------------------------------------------------------
    # On transforme la liste de codes en une liste de noms que l'on retourne

    liste_nom_pays = []
    for code_pays in liste_code_pays :
        liste_nom_pays += [data[code_pays]['Government']['Country name']['conventional short form']['text']]

    print("\nRésultats : \n")
    for code in range(len(liste_code_pays)) :
        print("• {} - {}".format(liste_nom_pays[code],information_pays(liste_code_pays[code])))

    input("\nAffichage terminé, appuyez sur Entrer pour continuer ")

    #------------------------------------------------------------------------------

    #------------------------------------------------------------------------------


# Problème : par rapport aux informations de certaines annees qui ne sont pas dans tous les pays























