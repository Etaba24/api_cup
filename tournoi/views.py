from django.shortcuts import render
from rest_framework import viewsets
from .models import Equipe, Match, Groupe
from .serializers import EquipeSerializer, MatchSerializer, GroupeSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import generer_matchs_de_poules, repartir_equipes_en_groupes, get_equipes_qualifiees, generer_phase_finale, generer_demi_finales, generer_finale

@api_view(['POST'])
def lancer_tirage(request):
    generer_matchs_de_poules()
    return Response({"message": "Tirage aléatoire des matchs de poule effectué avec succès."})
@api_view(['POST'])
def repartition_equipes(request):
    nb_groupes = request.data.get('nb_groupes', 4)  # 4 groupes par défaut
    repartir_equipes_en_groupes(nb_groupes)
    return Response({"message": f"Répartition aléatoire des équipes dans {nb_groupes} groupes réussie."})
@api_view(['POST'])
def generer_arbre_final(request):
    generer_phase_finale()
    return Response({"message": "Phase finale générée avec succès (quarts)."})
@api_view(['POST'])
def generer_demi(request):
    try:
        generer_demi_finales()
        return Response({"message": "Demi-finales générées avec succès."})
    except Exception as e:
        return Response({"erreur": str(e)}, status=400)
@api_view(['POST'])
def generer_finale_view(request):
    try:
        generer_finale()
        return Response({"message": "Finale (et petite finale) générée avec succès."})
    except Exception as e:
        return Response({"erreur": str(e)}, status=400)


class EquipeViewSet(viewsets.ModelViewSet):
    queryset = Equipe.objects.all()
    serializer_class = EquipeSerializer

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

class GroupeViewset(viewsets.ModelViewSet):
    queryset = Groupe.objects.all()
    serializer_class = GroupeSerializer
