from rest_framework import serializers
from .models import Badge, Score, AttributionBadge

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'


class ScoreSerializer(serializers.ModelSerializer):
    utilisateur = serializers.StringRelatedField()

    class Meta:
        model = Score
        fields = ['utilisateur', 'valeur', 'nb_exercices', 'last_updated']


class AttributionBadgeSerializer(serializers.ModelSerializer):
    utilisateur = serializers.StringRelatedField()
    badge = BadgeSerializer()

    class Meta:
        model = AttributionBadge
        fields = ['utilisateur', 'badge', 'date_obtention']
