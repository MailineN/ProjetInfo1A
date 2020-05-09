from pyfiglet import Figlet
from FonctionBD import clear

class Ouvert: 
    """Ensemble des méthodes permettant l'ouverture et l'affichage d'un menu 
    """    

    def __init__(self,previous_menu): 
        
        self.previous_menu = previous_menu 

    def run(self): 
        """ Déroulement du menu actuel

        Returns:
            actions[choix-1](self.previous_menu) -- Menu suivant sélectionné 
        """        
        clear()
        display = Figlet(font='big')
        print(display.renderText('Menu :'))
        print("༼ つ ಥ_ಥ ༽つ ༼ つ ಥ_ಥ ༽つ ༼ つ ಥ_ಥ ༽つ ༼ つ ಥ_ಥ ༽つ ༼ つ ಥ_ಥ ༽つ")
        print("\n")
        
        if len(self.previous_menu["path"]) != 0:
            chemin = self.previous_menu["path"][0]
            if len(self.previous_menu["path"]) > 2:
                for section in self.previous_menu["path"][2:]:
                    chemin += " -> {}".format(section)
            print("{} : {}\n".format(chemin, self.previous_menu["question"]))
        else : print("{:^63}\n".format(self.previous_menu["question"]))
        
        # Options et actions possibles 
        options = self.previous_menu["options"]
        nb_options = len(options)
        actions = self.previous_menu["actions"]
        
        # Affichage des options
        for i, opt in enumerate(options):
            print("• {} [{}]".format(opt,i+1))

        print('\n{:^63}\n'.format('Saisissez votre choix \n'))
        print("༼ つ ಥ_ಥ ༽つ ༼ つ ಥ_ಥ ༽つ ༼ つ ಥ_ಥ ༽つ ༼ つ ಥ_ಥ ༽つ ༼ つ ಥ_ಥ ༽つ \n")
        
        while True : 
            choix = input("Choix : ")
            try : 
                choix = int(choix)
            except ValueError : 
                print("Le choix doit être un entier.")
                continue

            if choix < 1 or choix > nb_options : 
                print(" La valeur doit être comprise entre 1 et {}.".format(nb_options))
                continue 
            break
        return actions[choix-1](self.previous_menu)

