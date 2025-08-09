from django.db import models

class Users(models.Model):
    id_user = models.AutoField(primary_key=True)
    names = models.TextField()
    email = models.CharField(max_length=30)
    pswd = models.TextField()
    role = models.TextField()

class Eleve(models.Model):
    id_eleve = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    levels = models.CharField(max_length=5, null=True)
    matricule_eleve = models.CharField(max_length=15)

class SessionApprentissage(models.Model):
    id_session = models.AutoField(primary_key=True)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)

class Resultat(models.Model):
    id_resultat = models.AutoField(primary_key=True)
    score = models.FloatField()
    nb_erreurs = models.IntegerField()
    temps_reponse = models.FloatField()
    date_soumission = models.DateTimeField()
    session = models.ForeignKey(SessionApprentissage, on_delete=models.CASCADE)
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE)
