from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Badge(models.Model):
    TITRE_CHOICES = [
        ("DÉBUTANT", "Débutant"),
        ("INTERMÉDIAIRE", "Intermédiaire"),
        ("EXPERT", "Expert"),
        ("PERSISTANT", "Persistant"),
        ("TOP1", "Top 1"),
    ]

    titre = models.CharField(max_length=50, choices=TITRE_CHOICES)
    description = models.TextField()
    image = models.ImageField(upload_to='badges/', null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre


class Score(models.Model):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)
    valeur = models.IntegerField(default=0)
    nb_exercices = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.utilisateur.username} — Score : {self.valeur}"


class AttributionBadge(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    date_obtention = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('utilisateur', 'badge')

    def __str__(self):
        return f"{self.utilisateur.username} a reçu {self.badge.titre}"
