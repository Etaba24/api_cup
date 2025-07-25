from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EquipeViewSet, MatchViewSet, GroupeViewset
from .views import lancer_tirage, repartition_equipes, generer_arbre_final, generer_demi, generer_finale_view

router = DefaultRouter()
router.register(r'equipes', EquipeViewSet)
router.register(r'matches', MatchViewSet)
router.register(r'groupes', GroupeViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('repartition/', repartition_equipes),
    path('lancer_tirage/', lancer_tirage),
    path('phase-finale/', generer_arbre_final),
    path('demi-finales/', generer_demi),
    path('finale/', generer_finale_view),
]
