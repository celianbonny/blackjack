import random


def obtenir_valeur(carte):
    """Renvoie la valeur en points d'une carte."""
    valeur = carte[0]
    if valeur in ['Valet', 'Dame', 'Roi']:
        return 10
    elif valeur == 'As':
        return 11  # Pour simplifier, l'As vaut 11 au départ
    else:
        return valeur


def calculer_score(main):
    """Calcule le score d'une main, en gérant les As qui valent 1 ou 11."""
    score = 0
    nombre_de_as = 0

    # On additionne la valeur de chaque carte
    for carte in main:
        score = score + obtenir_valeur(carte)
        if carte[0] == 'As':
            nombre_de_as = nombre_de_as + 1

    # Si on dépasse 21, on transforme des As de 11 en 1 (donc on enlève 10)
    while score > 21 and nombre_de_as > 0:
        score = score - 10
        nombre_de_as = nombre_de_as - 1

    return score


def creer_paquet():
    """Crée un paquet de 52 cartes mélangé (13 valeurs x 4 familles)."""
    # Correction : on retire le "1" qui faisait un doublon avec l'As
    valeurs = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Valet', 'Dame', 'Roi', 'As']
    familles = ['coeur', 'pic', 'trefle', 'carreau']
    paquet = []

    for famille in familles:
        for valeur in valeurs:
            paquet.append((valeur, famille))

    random.shuffle(paquet)
    return paquet


def demander_mise(argent):
    """Demande une mise au joueur et vérifie qu'elle est valide."""
    mise_valide = False
    mise = 0

    while mise_valide == False:
        texte_saisi = input(f"Combien voulez-vous miser ? (vous avez {argent}) : ")
        if texte_saisi.isdigit():
            mise = int(texte_saisi)
            if mise > 0 and mise <= argent:
                mise_valide = True
            else:
                print(f"Mise invalide. Elle doit être entre 1 et {argent}.")
        else:
            print("Veuillez entrer un nombre entier.")

    return mise


def tour_du_joueur(main_joueur, main_croupier, paquet, mise):
    """
    Gère le tour du joueur.
    Renvoie la main finale du joueur et la mise finale (qui peut avoir doublé).
    """
    en_jeu = True
    premier_tour = True
    mise_actuelle = mise

    while en_jeu:
        score_joueur = calculer_score(main_joueur)
        print(f"\nVos cartes : {main_joueur} | Votre score : {score_joueur}")
        print(f"Carte du croupier : {main_croupier[0]}")

        # Si le joueur a déjà dépassé 21, inutile de continuer à demander
        if score_joueur >= 21:
            en_jeu = False
        else:
            # Le "doubler" n'est proposé qu'au tout premier choix
            if premier_tour == True:
                doubler = input("Voulez-vous doubler ? (oui/non) : ").lower()
                if doubler == "oui":
                    main_joueur.append(paquet.pop())
                    mise_actuelle = mise_actuelle * 2
                    en_jeu = False  # Après un double, on ne tire qu'une seule carte
                else:
                    choix_carte = input("Voulez-vous une autre carte ? (oui/non) : ").lower()
                    if choix_carte == "oui":
                        main_joueur.append(paquet.pop())
                    else:
                        en_jeu = False
            else:
                choix_carte = input("Voulez-vous une autre carte ? (oui/non) : ").lower()
                if choix_carte == "oui":
                    main_joueur.append(paquet.pop())
                else:
                    en_jeu = False

        premier_tour = False

    return main_joueur, mise_actuelle


def jouer_une_manche(argent):
    """Joue une manche complète et renvoie le nouveau montant d'argent."""
    paquet = creer_paquet()
    mise = demander_mise(argent)
    print(f"Votre mise est de {mise}")

    # Distribution des cartes de départ
    main_joueur = [paquet.pop(), paquet.pop()]
    main_croupier = [paquet.pop(), paquet.pop()]

    # Tour du joueur
    main_joueur, mise = tour_du_joueur(main_joueur, main_croupier, paquet, mise)
    score_joueur = calculer_score(main_joueur)

    if score_joueur > 21:
        # Le joueur a dépassé 21 : inutile de faire jouer le croupier
        print(f"\nVos cartes : {main_joueur} (Score : {score_joueur})")
        print("Vous avez dépassé 21 ! Perdu.")
        argent = argent - mise
        print(f"Vous avez {argent} jetons")
        return argent

    # Tour du croupier (seulement si le joueur n'a pas dépassé 21)
    score_croupier = calculer_score(main_croupier)
    while score_croupier < 17:
        main_croupier.append(paquet.pop())
        score_croupier = calculer_score(main_croupier)

    # Résultats finaux
    print(f"\n--- Résultats ---")
    print(f"Vos cartes : {main_joueur} (Score : {score_joueur})")
    print(f"Cartes du croupier : {main_croupier} (Score : {score_croupier})")

    if score_croupier > 21:
        print("Le croupier a dépassé 21 ! Vous gagnez !")
        argent = argent + mise
    elif score_joueur > score_croupier:
        print("Vous gagnez !")
        argent = argent + mise
    elif score_joueur < score_croupier:
        print("Le croupier gagne.")
        argent = argent - mise
    else:
        print("Égalité !")

    print(f"Vous avez {argent} jetons")
    return argent


def jouer_blackjack():
    argent = 100
    print("----- Bienvenue au Blackjack ! -----")
    print(f"---vous avez {argent} jetons---")
    print("1. JOUER")
    print("2. QUITTER")

    choix = ""
    while choix not in ['1', '2']:
        choix = input("Choisissez 1 ou 2 : ")
        if choix not in ['1', '2']:
            print("Choix incorrect !")

    if choix == '2':
        print("Au revoir !")
    else:
        # On joue tant que le joueur a de l'argent
        while argent != 0:
            argent = jouer_une_manche(argent)

        print("Vous n'avez plus de jetons. Partie terminée.")


# Lancer le jeu
jouer_blackjack()