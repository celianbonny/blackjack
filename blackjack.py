import random

depart=100

def creer_paquet():
    #Crée un jeu de 52 cartes standard.
    couleurs = ['Cœur', 'Carreau', 'Trèfle', 'Pique']
    valeurs = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Valet', 'Dame', 'Roi', 'As']
    # Crée une liste de tuples (valeur, couleur)
    paquet = [(valeur, couleur) for couleur in couleurs for valeur in valeurs]
    random.shuffle(paquet)
    return paquet



print("1. JOUER")
print("2. QUITTER")

while True:
    choix = input("Choisissez 1 ou 2 : ")
    if choix in ['1', '2']:
        break
    else:
        print("Choix incorrect !")

print(f"Vous avez choisi l'option {choix}")

if choix=='1':
    print("vous avez 100 jetons")
    mise = int(input("choisie ta mise : "))
    print (f"vous avez mise {mise} jetons")
    gain = int(depart-mise)
    print(gain)
    print(paquet)

else : 
    print("relance")


