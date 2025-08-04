from django.db import models
from django.contrib.auth.models import AbstractUser

# Utilisateur personnalisé
class User(AbstractUser):
    # On peut déjà laisser ça vide pour l'instant ou ajouter un rôle plus tard
    is_rh = models.BooleanField(default=False)  # Ressources humaines ou simple employé

    def __str__(self):
        return self.username


# Dossier du personnel
class Employe(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    poste = models.CharField(max_length=100)
    date_embauche = models.DateField()
    salaire = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Dossier(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='dossiers')
    titre = models.CharField(max_length=255)
    fichier = models.FileField(upload_to='dossiers/')
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} - {self.employe.user.get_full_name()}"

