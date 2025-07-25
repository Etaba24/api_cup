import random
from .models import Equipe, Groupe, Match
from django.utils import timezone


def repartir_equipes_en_groupes(nb_groupes):
    # Récupérer toutes les équipes
    toutes_equipes = list(Equipe.objects.all())
    random.shuffle(toutes_equipes)

    # Supprimer les groupes et associations précédents (optionnel)
    Groupe.objects.all().delete()

    # Créer les groupes
    groupes = []
    for i in range(nb_groupes):
        groupe = Groupe.objects.create(nom=f'Groupe {chr(65+i)}')  # Groupe A, B, C, etc.
        groupes.append(groupe)

    # Répartir équitablement
    for index, equipe in enumerate(toutes_equipes):
        groupe_index = index % nb_groupes
        groupes[groupe_index].equipes.add(equipe)

def generer_matchs_de_poules():
    groupes = Groupe.objects.all()
    for groupe in groupes:
        equipes = list(groupe.equipes.all())
        random.shuffle(equipes)

        for i in range(len(equipes)):
            for j in range(i + 1, len(equipes)):
                Match.objects.create(
                    equipe1=equipes[i],
                    equipe2=equipes[j],
                    date=timezone.now(),
                    phase='POULES'
                )

def get_equipes_qualifiees():
    equipes_qualifiees = []

    groupes = Groupe.objects.all()
    for groupe in groupes:
        # Récupérer les matchs de poule du groupe
        equipes = list(groupe.equipes.all())

        scores = {equipe.id: 0 for equipe in equipes}

        # Calcul des scores
        matchs = Match.objects.filter(phase='POULES', equipe1__in=equipes, equipe2__in=equipes)
        for match in matchs:
            if match.score_equipe1 > match.score_equipe2:
                scores[match.equipe1.id] += 3
            elif match.score_equipe1 < match.score_equipe2:
                scores[match.equipe2.id] += 3
            else:
                scores[match.equipe1.id] += 1
                scores[match.equipe2.id] += 1

        # Trier les scores
        equipes_sorted = sorted(equipes, key=lambda e: scores[e.id], reverse=True)
        equipes_qualifiees.extend(equipes_sorted[:2])  # Prendre les 2 meilleures

    return equipes_qualifiees

def generer_phase_finale():
    qualifiees = get_equipes_qualifiees()
    random.shuffle(qualifiees)

    # QUARTS
    for i in range(0, len(qualifiees), 2):
        Match.objects.create(
            equipe1=qualifiees[i],
            equipe2=qualifiees[i+1],
            date=timezone.now(),
            phase='QUART'
        )

def generer_demi_finales():
    # Récupère tous les matchs de quart de finale
    quarts = Match.objects.filter(phase='QUART')
    vainqueurs = []

    for match in quarts:
        if match.score_equipe1 > match.score_equipe2:
            vainqueurs.append(match.equipe1)
        elif match.score_equipe2 > match.score_equipe1:
            vainqueurs.append(match.equipe2)
        else:
            # Cas d’égalité, à gérer selon règles (ici on ignore)
            continue

    if len(vainqueurs) != 4:
        raise Exception("Il faut 4 vainqueurs pour les demi-finales")

    random.shuffle(vainqueurs)

    # Génère 2 demi-finales
    for i in range(0, 4, 2):
        Match.objects.create(
            equipe1=vainqueurs[i],
            equipe2=vainqueurs[i+1],
            date=timezone.now(),
            phase='DEMI'
        )

def generer_finale():
    demi_matchs = Match.objects.filter(phase='DEMI')
    finalistes = []
    troisiemes = []

    for match in demi_matchs:
        if match.score_equipe1 > match.score_equipe2:
            finalistes.append(match.equipe1)
            troisiemes.append(match.equipe2)
        elif match.score_equipe2 > match.score_equipe1:
            finalistes.append(match.equipe2)
            troisiemes.append(match.equipe1)

    if len(finalistes) != 2:
        raise Exception("Il faut 2 finalistes pour créer la finale")

    # Création de la finale
    Match.objects.create(
        equipe1=finalistes[0],
        equipe2=finalistes[1],
        date=timezone.now(),
        phase='FINALE'
    )

    # Optionnel : petite finale (3e place)
    if len(troisiemes) == 2:
        Match.objects.create(
            equipe1=troisiemes[0],
            equipe2=troisiemes[1],
            date=timezone.now(),
            phase='PETITE_FINALE'
        )
