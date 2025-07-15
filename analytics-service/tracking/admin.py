from django.contrib import admin
from . import models

admin.site.register(models.Users)
admin.site.register(models.Eleve)
admin.site.register(models.SessionApprentissage)
admin.site.register(models.Resultat)
