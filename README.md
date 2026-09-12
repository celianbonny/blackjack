# Blackjack (TP5)

Un jeu de Blackjack en console, écrit en Python.

## Description

Ce projet implémente le jeu de Blackjack de base, ainsi que plusieurs
règles additionnelles classiques du casino (mise variable, assurance,
persistance de l'argent...).

Au Blackjack, l'objectif est d'obtenir une main la plus proche possible
de 21 points, sans le dépasser, et de battre la main de la banque.

## Prérequis

- Python 3 (aucune bibliothèque externe n'est nécessaire, seul le module
  `random` de la bibliothèque standard est utilisé)

## Lancer le jeu

Depuis un terminal, dans le dossier du projet :

```bash
python3 blackjack.py
```

## Règles implémentées

### Jeu de base

- Distribution de 2 cartes au joueur et à la banque (une seule carte de
  la banque est visible)
- Le joueur peut tirer autant de cartes qu'il le souhaite, tant qu'il ne
  dépasse pas 21
- Le joueur peut doubler sa mise avant de tirer d'autres cartes (une
  seule carte supplémentaire est alors distribuée)
- La banque tire des cartes tant que son score est inférieur à 17
- Les gains sont calculés selon le tableau officiel des résultats
  (perte, égalité, gain de 1 pour 1, gain de 3 pour 2 pour un Blackjack)

### Fonctionnalités additionnelles

- **Persistance entre les manches** : l'argent du joueur est conservé
  d'une manche à l'autre au sein d'une même partie.
- **Persistance entre les parties** : l'argent est sauvegardé dans un
  fichier (`argent.txt`) et rechargé automatiquement au lancement
  suivant du jeu. Si le fichier n'existe pas encore, le joueur démarre
  avec 100 jetons.
- **Mise variable** : le joueur choisit librement sa mise, entre une
  mise minimale et une mise maximale définies par le casino. À chaque
  victoire, la mise maximale autorisée est doublée pour la manche
  suivante.
- **Assurance** : si la première carte visible de la banque est un As,
  le joueur peut prendre une assurance, dont le coût est égal à la
  moitié (arrondie au supérieur) de sa mise de départ. Si la banque a
  effectivement un Blackjack, l'assurance rapporte le double de sa
  mise ; sinon, elle est perdue.
- **Possibilité de quitter en cours de partie** : après chaque manche,
  le joueur peut choisir d'arrêter de jouer sans devoir attendre de
  n'avoir plus de jetons.

## Fonctionnalités non encore implémentées

Les extensions suivantes, décrites dans le sujet, ne sont pas (encore)
présentes dans cette version :

- Joueurs supplémentaires (section 2.5)
- Split (section 2.6)
- Intelligence des joueurs (section 3.1)
- Statistiques de parties (section 3.2)

## Structure du fichier

Le jeu est organisé en plusieurs fonctions, chacune responsable d'une
tâche précise :

| Fonction | Rôle |
| --- | --- |
| `charger_argent` / `sauvegarder_argent` | Lecture et écriture de l'argent dans le fichier de sauvegarde |
| `obtenir_valeur` | Valeur en points d'une carte |
| `calculer_score` | Score total d'une main (gère les As à 1 ou 11) |
| `creer_paquet` | Création et mélange d'un paquet de 52 cartes |
| `categoriser_main` | Catégorie d'une main selon le tableau des gains |
| `rang_categorie` | Classement numérique d'une catégorie |
| `determiner_resultat` | Résultat d'une manche (perte, égalité, gain...) |
| `demander_mise` | Demande et validation de la mise du joueur |
| `demander_assurance` | Proposition et gestion de l'assurance |
| `tour_du_joueur` | Déroulement du tour du joueur (doubler, tirer) |
| `jouer_une_manche` | Déroulement complet d'une manche |
| `jouer_blackjack` | Boucle principale et menu du jeu |

## Sauvegarde

Le fichier `argent.txt` est créé automatiquement dans le même dossier
que le script, dès la première manche jouée. Il contient uniquement le
nombre de jetons actuellement possédés par le joueur.