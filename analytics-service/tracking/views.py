# from urllib import request
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Resultat, Eleve
from .serializers import ResultatSerializer
from django.db.models import Avg, Count, Sum
# from django.http import HttpResponse
from datetime import datetime

class AjouterResultat(APIView):
    def post(self, request):
        serializer = ResultatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Résultat enregistré"}, status=201)
        return Response(serializer.errors, status=400)

class PerformanceEleveView(APIView):
    def get(self, request, eleve_id):
        try:
            resultats = Resultat.objects.filter(eleve_id=eleve_id)

            if not resultats.exists():
                return Response({"message": "Aucun résultat trouvé pour cet élève"}, status=404)

            stats = resultats.aggregate(
                moyenne_score=Avg('score'),
                total_exercices=Count('id_resultat'),
                total_erreurs=Sum('nb_erreurs'),
                moyenne_temps=Avg('temps_reponse')
            )

            return Response({
                "eleve_id": eleve_id,
                "moyenne_score": stats['moyenne_score'],
                "total_exercices": stats['total_exercices'],
                "total_erreurs": stats['total_erreurs'],
                "temps_reponse_moyen": stats['moyenne_temps']
            })

        except Eleve.DoesNotExist:
            return Response({"message": "Élève introuvable"}, status=404)
        
# def test_view(request):
#     return render(request, "index.html")

def test(request, page):
    date = datetime.today()
    return render(request, f"analytics/{page}.html", context={"date_time": date})

# def about(request):
#     return render(request, "analytics/about.html", context={"date": datetime.today()})
