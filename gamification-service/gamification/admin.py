from django.contrib import admin
from .models import Badge, Score, AttributionBadge

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('titre', 'description', 'date_creation')
    search_fields = ('titre',)
    list_filter = ('date_creation',)

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'valeur', 'nb_exercices', 'last_updated')
    search_fields = ('utilisateur__username',)

@admin.register(AttributionBadge)
class AttributionBadgeAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'badge', 'date_obtention')
    search_fields = ('utilisateur__username', 'badge__titre')
    list_filter = ('badge', 'date_obtention')
