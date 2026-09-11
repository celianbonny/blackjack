import random

def creer_paquet():
    # Crée un paquet de cartes simple (valeurs de 1 à 10 pour simplifier)
    valeurs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    famille = ['coeur', 'pic', 'trefle', 'carreau']
    paquet = []
    
    # On ajoute plusieurs fois les valeurs pour faire un paquet
    for i in range(4):
        for v in valeurs:
            paquet.append(v)  
    random.shuffle(paquet)
    return paquet

def jouer_blackjack():
    print("--- Bienvenue au Blackjack ! ---")
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
        paquet = creer_paquet()
        
        # Distribution des cartes de départ
        main_joueur = [paquet.pop(), paquet.pop()]
        main_croupier = [paquet.pop(), paquet.pop()]
        
        # Tour du joueur
        en_jeu = True
        while en_jeu:
            score_joueur = sum(main_joueur)
            print(f"\nVos cartes : {main_joueur} | Votre score : {score_joueur}")
            print(f"Carte du croupier : {main_croupier[0]}")
            
            if score_joueur > 21:
                print("Vous avez dépassé 21 ! Perdu.")
                return
                
            choix = input("Voulez-vous une autre carte ? (oui/non) : ").lower()
            if choix == "oui":
                main_joueur.append(paquet.pop())
            else:
                en_jeu = False
                
        # Tour du croupier
        score_croupier = sum(main_croupier)
        while score_croupier < 17:
            main_croupier.append(paquet.pop())
            score_croupier = sum(main_croupier)
            
        # Résultats finaux
        score_joueur = sum(main_joueur)
        print(f"\n--- Résultats ---")
        print(f"Vos cartes : {main_joueur} (Score : {score_joueur})")
        print(f"Cartes du croupier : {main_croupier} (Score : {score_croupier})")
        
        if score_croupier > 21:
            print("Le croupier a dépassé 21 ! Vous gagnez !")
        elif score_joueur > score_croupier:
            print("Vous gagnez !")
        elif score_joueur < score_croupier:
            print("Le croupier gagne.")
        else:
            print("Égalité !")
    else : 
        print ("au revoir")
# Lancer le jeu
jouer_blackjack()