import random

def obtenir_valeur(carte):
    valeur = carte[0]
    if valeur in ['Valet', 'Dame', 'Roi']:
        return 10
    elif valeur == 'As':
        return 11 # Pour simplifier, l'As vaut 11 ici
    else:
        return valeur

def calculer_score(main):
    score = sum(obtenir_valeur(carte) for carte in main)
    # Gestion simple des As si on dépasse 21
    as_count = sum(1 for carte in main if carte[0] == 'As')
    while score > 21 and as_count > 0:
        score -= 10
        as_count -= 1
    return score

def creer_paquet():
    # Crée un paquet de cartes simple
    valeurs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'Valet', 'Dame', 'Roi', 'As']
    familles = ['coeur', 'pic', 'trefle', 'carreau']
    paquet = []
    
    for famille in familles:
        for valeur in valeurs:
            paquet.append((valeur, famille)) 
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
    if choix == '1':
        paquet = creer_paquet()
        
        # Distribution des cartes de départ
        main_joueur = [paquet.pop(), paquet.pop()]
        main_croupier = [paquet.pop(), paquet.pop()]
        
        # Tour du joueur
        en_jeu = True
        duble = 0
        while en_jeu:
            score_joueur = calculer_score(main_joueur)
            print(f"\nVos cartes : {main_joueur} | Votre score : {score_joueur}")
            print(f"Carte du croupier : {main_croupier[0]}")
            
            if score_joueur > 21:
                print("Vous avez dépassé 21 ! Perdu.")
                return

            doubler = input("Voulez-vous doubler ? (oui/non) : ").lower()
            if doubler == "oui":
                main_joueur.append(paquet.pop())
                duble = 1
            else:
                en_jeu = False

            if (duble ==0):                    
                choix_carte = input("Voulez-vous une autre carte ? (oui/non) : ").lower()
                if choix_carte == "oui":
                    main_joueur.append(paquet.pop())
                else:
                    en_jeu = False
            else: 
                en_jeu = False
                
        # Tour du croupier
        score_croupier = calculer_score(main_croupier)
        while score_croupier < 17:
            main_croupier.append(paquet.pop())
            score_croupier = calculer_score(main_croupier)
            
        # Résultats finaux
        score_joueur = calculer_score(main_joueur)
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
    else:
        print("Au revoir")

# Lancer le jeu
jouer_blackjack()