from rest_framework import serializers
from .models import Resultat

class ResultatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resultat
        fields = '__all__'
