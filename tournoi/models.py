from django.db import models

# Create your models here.
class Equipe(models.Model):
    nom = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    # ville = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom

class Groupe(models.Model):
    nom = models.CharField(max_length=1)  # A, B, C...
    equipes = models.ManyToManyField(Equipe, related_name='groupes')

    def __str__(self):
        return f"Groupe {self.nom}"

class Match(models.Model): 
    equipe1 = models.ForeignKey(Equipe, related_name='matchs_equipe1', on_delete=models.CASCADE)
    equipe2 = models.ForeignKey(Equipe, related_name='matchs_equipe2', on_delete=models.CASCADE)
    date = models.DateTimeField(null=True, blank=True)
    score_equipe1 = models.IntegerField(default=0)
    score_equipe2 = models.IntegerField(default=0)
    phase = models.CharField(max_length=20, choices=[
        ('POULES', 'Phases de poules'),
        ('QUART', 'Quart de finale'),
        ('DEMI', 'Demi-finale'),
        ('FINALE', 'Finale'),
    ])

    def __str__(self):
        return f"{self.equipe1} vs {self.equipe2} ({self.phase})"
