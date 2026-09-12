import random

# Nom du fichier où l'on sauvegarde l'argent du joueur entre les parties
FICHIER_SAUVEGARDE = "argent.txt"

# Règles du casino pour la mise variable (2.3)
MISE_MINIMALE = 5
MISE_MAXIMALE_DE_DEPART = 50


def charger_argent():
    """
    Lit l'argent sauvegardé dans le fichier de sauvegarde.
    Si le fichier n'existe pas encore (première fois qu'on joue),
    on démarre avec 100 jetons.
    """
    try:
        fichier = open(FICHIER_SAUVEGARDE, "r")
        contenu = fichier.read()
        fichier.close()
        argent = int(contenu)
        return argent
    except:
        return 100


def sauvegarder_argent(argent):
    """Écrit l'argent actuel dans le fichier de sauvegarde."""
    fichier = open(FICHIER_SAUVEGARDE, "w")
    fichier.write(str(argent))
    fichier.close()


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


def categoriser_main(main, score):
    """
    Détermine la catégorie d'une main, comme dans le tableau des gains :
    "Supérieur à 21", "Blackjack", "21", "20", "19", "18", "17" ou "Inférieur à 17".
    Un Blackjack, c'est un score de 21 obtenu avec seulement 2 cartes.
    """
    if score > 21:
        return "Supérieur à 21"
    elif score == 21 and len(main) == 2:
        return "Blackjack"
    elif score == 21:
        return "21"
    elif score == 20:
        return "20"
    elif score == 19:
        return "19"
    elif score == 18:
        return "18"
    elif score == 17:
        return "17"
    else:
        return "Inférieur à 17"


def rang_categorie(categorie):
    """
    Donne un rang numérique à une catégorie, pour pouvoir comparer deux mains.
    Plus le rang est élevé, meilleure est la main.
    (Ne sert pas pour "Supérieur à 21", qui est géré à part.)
    """
    if categorie == "Blackjack":
        return 6
    elif categorie == "21":
        return 5
    elif categorie == "20":
        return 4
    elif categorie == "19":
        return 3
    elif categorie == "18":
        return 2
    elif categorie == "17":
        return 1
    else:  # "Inférieur à 17"
        return 0


def determiner_resultat(main_joueur, score_joueur, main_croupier, score_croupier):
    """
    Applique le tableau officiel des gains et renvoie un mot-clé :
    "perte", "egalite", "gain_1_pour_1" ou "gain_3_pour_2".
    """
    categorie_joueur = categoriser_main(main_joueur, score_joueur)
    categorie_croupier = categoriser_main(main_croupier, score_croupier)

    # Règle 1 : si le joueur dépasse 21, il perd toujours,
    # même si la banque dépasse 21 elle aussi
    if categorie_joueur == "Supérieur à 21":
        return "perte"

    # Règle 2 : la banque dépasse 21, mais pas le joueur : le joueur gagne
    if categorie_croupier == "Supérieur à 21":
        if categorie_joueur == "Blackjack":
            return "gain_3_pour_2"
        else:
            return "gain_1_pour_1"

    # Règle 3 : ni l'un ni l'autre ne dépasse 21, on compare les catégories
    rang_joueur = rang_categorie(categorie_joueur)
    rang_croupier = rang_categorie(categorie_croupier)

    if rang_joueur > rang_croupier:
        if categorie_joueur == "Blackjack":
            return "gain_3_pour_2"
        else:
            return "gain_1_pour_1"
    elif rang_joueur == rang_croupier:
        return "egalite"
    else:
        return "perte"


def demander_mise(argent, mise_minimale, mise_maximale):
    """
    Demande une mise au joueur, comprise entre la mise minimale et la mise
    maximale du casino, sans jamais dépasser l'argent que possède le joueur.
    """
    # On ne peut pas demander plus que ce que le joueur possède
    minimum_effectif = mise_minimale
    maximum_effectif = mise_maximale

    if maximum_effectif > argent:
        maximum_effectif = argent
    if minimum_effectif > argent:
        minimum_effectif = argent  # Le joueur doit alors miser tout ce qu'il lui reste

    mise_valide = False
    mise = 0

    while mise_valide == False:
        texte_saisi = input(
            f"Combien voulez-vous miser ? (entre {minimum_effectif} et {maximum_effectif}) : "
        )
        if texte_saisi.isdigit():
            mise = int(texte_saisi)
            if mise >= minimum_effectif and mise <= maximum_effectif:
                mise_valide = True
            else:
                print(f"Mise invalide. Elle doit être entre {minimum_effectif} et {maximum_effectif}.")
        else:
            print("Veuillez entrer un nombre entier.")

    return mise


def demander_assurance(main_croupier, mise_depart, argent):
    """
    Si la première carte de la banque est un As, propose une assurance au joueur.
    Renvoie un tuple (a_pris_assurance, cout_assurance).
    Le coût de l'assurance est la moitié de la mise de départ, arrondie au supérieur.
    """
    premiere_carte_banque = main_croupier[0]

    if premiere_carte_banque[0] != 'As':
        return False, 0

    # Arrondi au supérieur sans utiliser de module externe : (mise + 1) // 2
    cout_assurance = (mise_depart + 1) // 2

    if argent < cout_assurance:
        print("(Vous n'avez pas assez de jetons pour prendre une assurance)")
        return False, 0

    reponse = input(
        f"La banque montre un As. Voulez-vous prendre une assurance pour {cout_assurance} jetons ? (oui/non) : "
    ).lower()

    if reponse == "oui":
        return True, cout_assurance
    else:
        return False, 0


def tour_du_joueur(main_joueur, main_croupier, paquet, mise, argent):
    """
    Gère le tour du joueur.
    Renvoie la main finale du joueur et la mise finale (qui peut avoir doublé).
    """
    mise_actuelle = mise
    a_double = False

    score_joueur = calculer_score(main_joueur)
    print(f"\nVos cartes : {main_joueur} | Votre score : {score_joueur}")
    print(f"Carte du croupier : {main_croupier[0]}")

    # Étape 1 : la question du double n'est posée qu'une seule fois,
    # avant tout tirage de carte supplémentaire
    if score_joueur < 21:
        peut_doubler = argent >= mise_actuelle * 2

        if peut_doubler == True:
            doubler = input("Voulez-vous doubler ? (oui/non) : ").lower()
        else:
            print("(Vous n'avez pas assez de jetons pour doubler)")
            doubler = "non"

        if doubler == "oui":
            main_joueur.append(paquet.pop())
            mise_actuelle = mise_actuelle * 2
            a_double = True
            score_joueur = calculer_score(main_joueur)
            print(f"\nVos cartes : {main_joueur} | Votre score : {score_joueur}")

    # Étape 2 : si le joueur n'a pas doublé, il peut tirer
    # autant de cartes qu'il le souhaite, une par une
    if a_double == False:
        en_jeu = True
        while en_jeu:
            score_joueur = calculer_score(main_joueur)

            if score_joueur >= 21:
                en_jeu = False
            else:
                choix_carte = input("Voulez-vous une autre carte ? (oui/non) : ").lower()
                if choix_carte == "oui":
                    main_joueur.append(paquet.pop())
                    score_joueur = calculer_score(main_joueur)
                    print(f"\nVos cartes : {main_joueur} | Votre score : {score_joueur}")
                    print(f"Carte du croupier : {main_croupier[0]}")
                else:
                    en_jeu = False

    return main_joueur, mise_actuelle


def jouer_une_manche(argent, mise_minimale, mise_maximale):
    """
    Joue une manche complète.
    Renvoie le nouveau montant d'argent et la nouvelle mise maximale
    (qui double à chaque victoire du joueur).
    """
    paquet = creer_paquet()
    mise = demander_mise(argent, mise_minimale, mise_maximale)
    print(f"Votre mise est de {mise}")

    # Distribution des cartes de départ
    main_joueur = [paquet.pop(), paquet.pop()]
    main_croupier = [paquet.pop(), paquet.pop()]

    # Proposition d'assurance si la banque montre un As
    a_pris_assurance, cout_assurance = demander_assurance(main_croupier, mise, argent)
    if a_pris_assurance == True:
        argent = argent - cout_assurance

    # Tour du joueur
    main_joueur, mise = tour_du_joueur(main_joueur, main_croupier, paquet, mise, argent)
    score_joueur = calculer_score(main_joueur)

    # Tour du croupier (seulement si le joueur n'a pas dépassé 21 :
    # si le joueur a déjà perdu, inutile de faire tirer la banque)
    if score_joueur <= 21:
        score_croupier = calculer_score(main_croupier)
        while score_croupier < 17:
            main_croupier.append(paquet.pop())
            score_croupier = calculer_score(main_croupier)

    score_croupier = calculer_score(main_croupier)

    # Résultats finaux
    print(f"\n--- Résultats ---")
    print(f"Vos cartes : {main_joueur} (Score : {score_joueur})")
    print(f"Cartes du croupier : {main_croupier} (Score : {score_croupier})")

    # Résolution de l'assurance, indépendamment du reste
    if a_pris_assurance == True:
        categorie_croupier = categoriser_main(main_croupier, score_croupier)
        if categorie_croupier == "Blackjack":
            gain_assurance = cout_assurance * 2
            print(f"La banque a un Blackjack ! Votre assurance vous rapporte {gain_assurance} jetons.")
            argent = argent + gain_assurance
        else:
            print("La banque n'a pas de Blackjack. Vous perdez votre assurance.")

    resultat = determiner_resultat(main_joueur, score_joueur, main_croupier, score_croupier)

    if resultat == "perte":
        print("Vous perdez.")
        argent = argent - mise
    elif resultat == "egalite":
        print("Égalité !")
        # L'argent ne change pas
    elif resultat == "gain_1_pour_1":
        print("Vous gagnez ! (gain de 1 pour 1)")
        argent = argent + mise
        mise_maximale = mise_maximale * 2  # La mise maximale double à chaque victoire
    elif resultat == "gain_3_pour_2":
        # Gain de 3 pour 2 : on arrondit à l'entier inférieur
        gain = (mise * 3) // 2
        print(f"Blackjack ! Vous gagnez {gain} jetons (gain de 3 pour 2)")
        argent = argent + gain
        mise_maximale = mise_maximale * 2  # La mise maximale double à chaque victoire

    print(f"Vous avez {argent} jetons")
    return argent, mise_maximale


def jouer_blackjack():
    argent = charger_argent()
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
        # On joue tant que le joueur a de l'argent ET qu'il veut continuer
        continuer_a_jouer = True
        mise_maximale = MISE_MAXIMALE_DE_DEPART

        while argent != 0 and continuer_a_jouer == True:
            argent, mise_maximale = jouer_une_manche(argent, MISE_MINIMALE, mise_maximale)
            sauvegarder_argent(argent)  # On sauvegarde après chaque manche

            # On ne propose de quitter que s'il reste des jetons
            # (sinon la partie s'arrête de toute façon)
            if argent != 0:
                reponse = input("\nVoulez-vous continuer à jouer ? (oui/non) : ").lower()
                if reponse != "oui":
                    continuer_a_jouer = False

        if argent == 0:
            print("Vous n'avez plus de jetons. Partie terminée.")
        else:
            print(f"Au revoir ! Vous quittez avec {argent} jetons.")


# Lancer le jeu (seulement si on exécute ce fichier directement)
if __name__ == "__main__":
    jouer_blackjack()