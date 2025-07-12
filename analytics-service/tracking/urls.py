from django.urls import path
from .views import AjouterResultat
from .views import PerformanceEleveView

urlpatterns = [
    path('ajouter-resultat/', AjouterResultat.as_view(), name='ajouter-resultat'),
    path('eleve/<int:eleve_id>/performances/', PerformanceEleveView.as_view(), name='performance-eleve'),
]