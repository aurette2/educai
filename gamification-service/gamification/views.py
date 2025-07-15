from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Badge, Score, AttributionBadge
from .serializers import BadgeSerializer, ScoreSerializer, AttributionBadgeSerializer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated


User = get_user_model()

# Liste des badges attribués à un utilisateur
class UserBadgesView(generics.ListAPIView):
    serializer_class = AttributionBadgeSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return AttributionBadge.objects.filter(utilisateur__id=user_id)


# Voir le score d’un utilisateur
class UserScoreView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ScoreSerializer
    lookup_field = 'utilisateur_id'
    queryset = Score.objects.all()


# Attribuer un badge à un utilisateur
class AssignBadgeView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        badge_id = request.data.get("badge_id")

        utilisateur = get_object_or_404(User, id=user_id)
        badge = get_object_or_404(Badge, id=badge_id)

        # Vérifie s’il n’a pas déjà ce badge
        if AttributionBadge.objects.filter(utilisateur=utilisateur, badge=badge).exists():
            return Response({"message": "Badge déjà attribué"}, status=400)

        AttributionBadge.objects.create(utilisateur=utilisateur, badge=badge)
        return Response({"message": "Badge attribué avec succès"}, status=201)

class UpdateScoreView(APIView):
    permission_classes = [AllowAny]  # à restreindre plus tard selon ton auth

    def post(self, request):
        user_id = request.data.get("user_id")
        points = int(request.data.get("points", 0))  # Points à ajouter

        utilisateur = get_object_or_404(User, id=user_id)

        # Récupérer ou créer un score
        score_obj, created = Score.objects.get_or_create(utilisateur=utilisateur)

        score_obj.valeur += points
        score_obj.nb_exercices += 1
        score_obj.save()

        # Vérifier si on doit attribuer un badge "Débutant"
        if score_obj.nb_exercices == 5:
            badge, _ = Badge.objects.get_or_create(titre="DÉBUTANT", defaults={
                'description': "Tu as terminé 5 exercices. Bravo !"
            })
            AttributionBadge.objects.get_or_create(utilisateur=utilisateur, badge=badge)

        return Response({
            "message": "Score mis à jour",
            "score": score_obj.valeur,
            "nb_exercices": score_obj.nb_exercices
        }, status=200)