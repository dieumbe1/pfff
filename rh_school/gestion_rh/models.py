from django.db import models
from django.contrib.auth.models import User

# =========================================================
# 0. PROFIL UTILISATEUR : ROLE (EMPLOYE / RH)
# =========================================================

class ProfilUtilisateur(models.Model):
    ROLE_CHOICES = (
        ('EMPLOYE', 'Employé'),
        ('RH', 'Responsable RH'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='EMPLOYE')

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


# =========================================================
# 1. PARAMÈTRES ET STRUCTURE DE BASE
# =========================================================

class Departement(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    date_fin = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Départements"

    def __str__(self):
        return self.nom


class Employe(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='employe', null=True, blank=True
    )
    matricule = models.CharField(max_length=10, primary_key=True)
    nom = models.CharField(max_length=40)
    prenom = models.CharField(max_length=30)
    sexe = models.CharField(max_length=1, choices=[('M', 'Masculin'), ('F', 'Féminin')])
    date_naissance = models.DateField()
    email = models.EmailField(max_length=50, unique=True)
    telephone = models.CharField(max_length=15)
    adresse = models.CharField(max_length=255, default='Non renseignée')
    date_embauche = models.DateField()
    departement = models.ForeignKey(
        Departement, on_delete=models.PROTECT, related_name='employes', null=True, blank=True
    )

    class Meta:
        verbose_name = "Employé"
        verbose_name_plural = "Employés"
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"{self.matricule} - {self.nom} {self.prenom}"


# =========================================================
# 2. GESTION DES RESSOURCES
# =========================================================

class Formation(models.Model):
    intitule_formation = models.CharField(max_length=100)
    organisme = models.CharField(max_length=100)
    date_formation = models.DateField()
    cout = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    personnel_suivi = models.ManyToManyField(
        Employe, related_name='formations_suivies', blank=True
    )

    class Meta:
        verbose_name = "Formation"
        verbose_name_plural = "Formations"

    def __str__(self):
        return self.intitule_formation


class Contrat(models.Model):
    TYPE_CHOICES = [
        ('CDI', 'Contrat à Durée Indéterminée'),
        ('CDD', 'Contrat à Durée Déterminée'),
        ('STAGE', 'Stage'),
    ]
    type_contrat = models.CharField(max_length=10, choices=TYPE_CHOICES)
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='contrats')

    class Meta:
        verbose_name = "Contrat"
        verbose_name_plural = "Contrats"

    def __str__(self):
        return f"{self.get_type_contrat_display()} - {self.employe.nom} {self.employe.prenom}"


class Salaire(models.Model):
    employe = models.ForeignKey(
        Employe, on_delete=models.CASCADE, related_name='salaires', null=True
    )
    montant_base = models.DecimalField(max_digits=10, decimal_places=2)
    montant_net = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    date_effective = models.DateField(null=True, blank=True)
    periode = models.CharField(max_length=50, default='Mensuel')

    class Meta:
        verbose_name = "Salaire"
        verbose_name_plural = "Salaires"
        ordering = ['-date_effective']

    def __str__(self):
        nom = self.employe.nom if self.employe else "Inconnu"
        return f"{self.periode} - {nom} ({self.montant_net} €)"


# =========================================================
# 3. GESTION DU TEMPS ET DES ABSENCES
# =========================================================

class Conge(models.Model):
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En Attente'),
        ('APPROUVE', 'Approuvé'),
        ('REJETE', 'Rejeté'),
    ]

    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='conges')
    date_debut = models.DateField()
    date_fin = models.DateField()
    motif = models.TextField(max_length=500, default='Vacances annuelles')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_ATTENTE')
    date_demande = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Congé"
        verbose_name_plural = "Congés"

    def __str__(self):
        return f"{self.employe.nom} - {self.date_debut} au {self.date_fin} ({self.get_statut_display()})"


class JourDeTravail(models.Model):
    jour = models.CharField(max_length=50)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    statut = models.CharField(max_length=50, default='Standard')
    employes = models.ManyToManyField(Employe, related_name='horaires', blank=True)

    class Meta:
        verbose_name = "Jour de Travail"
        verbose_name_plural = "Jours de Travail"

    def __str__(self):
        return f"{self.jour} ({self.heure_debut.strftime('%H:%M')} - {self.heure_fin.strftime('%H:%M')})"
