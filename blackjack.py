print("1. JOUER")
print("2. QUITTER")

while True:
    choix = input("Choisissez 1 ou 2 : ")
    if choix in ['1', '2']:
        break
    else:
        print("Choix incorrect !")

print(f"Vous avez choisi l'option {choix}")

if (choix==1):
    print("vous avez 100 jetons")

