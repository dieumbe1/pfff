from django.db import models
from django.db.models.functions import Lower
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Departement(models.Model):
    nom = models.CharField(max_length=100, unique=True, verbose_name='Nom du département')
    description = models.TextField(blank=True, verbose_name='Description')
    responsable = models.ForeignKey('Employe', on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='departements_diriges', verbose_name='Responsable')
    budget_annuel = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, 
                                       verbose_name='Budget annuel')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    actif = models.BooleanField(default=True, verbose_name='Actif')
    
    class Meta:
        verbose_name = 'Département'
        verbose_name_plural = 'Départements'
        ordering = ['nom']
        constraints = [
            models.UniqueConstraint(Lower('nom'), name='unique_departement_nom_ci')
        ]
    
    def __str__(self):
        return self.nom
    
    def nombre_employes(self):
        return self.employes.count()

class Employe(models.Model):
    ROLE_CHOICES = [
        ('RH', 'Responsable RH'),
        ('EMPLOYE', 'Employé'),
    ]
    
    STATUT_CHOICES = [
        ('ACTIF', 'Actif'),
        ('INACTIF', 'Inactif'),
        ('CONGE', 'En congé'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employe')
    matricule = models.CharField(max_length=20, unique=True, verbose_name='Matricule')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='EMPLOYE', verbose_name='Rôle')
    nom = models.CharField(max_length=100, verbose_name='Nom')
    prenom = models.CharField(max_length=100, verbose_name='Prénom')
    email = models.EmailField(unique=True, verbose_name='Email')
    telephone = models.CharField(max_length=20, verbose_name='Téléphone')
    adresse = models.TextField(verbose_name='Adresse')
    date_naissance = models.DateField(verbose_name='Date de naissance')
    date_embauche = models.DateField(verbose_name="Date d'embauche")
    poste = models.CharField(max_length=100, verbose_name='Poste')
    departement = models.ForeignKey(Departement, on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='employes', verbose_name='Département')
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='ACTIF', verbose_name='Statut')
    photo = models.ImageField(upload_to='employes/', blank=True, null=True, verbose_name='Photo')
    
    class Meta:
        verbose_name = 'Employé'
        verbose_name_plural = 'Employés'
        ordering = ['nom', 'prenom']
    
    def __str__(self):
        return f"{self.matricule} - {self.nom} {self.prenom}"
    
    def get_full_name(self):
        return f"{self.prenom} {self.nom}"

class Formation(models.Model):
    STATUT_CHOICES = [
        ('PROGRAMMEE', 'Programmée'),
        ('EN_COURS', 'En cours'),
        ('TERMINEE', 'Terminée'),
        ('ANNULEE', 'Annulée'),
    ]
    
    titre = models.CharField(max_length=200, verbose_name='Titre')
    description = models.TextField(verbose_name='Description')
    date_debut = models.DateField(verbose_name='Date de début')
    date_fin = models.DateField(verbose_name='Date de fin')
    lieu = models.CharField(max_length=200, verbose_name='Lieu')
    formateur = models.CharField(max_length=100, verbose_name='Formateur')
    capacite = models.IntegerField(verbose_name='Capacité maximale', validators=[MinValueValidator(1)])
    statut = models.CharField(max_length=15, choices=STATUT_CHOICES, default='PROGRAMMEE', verbose_name='Statut')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    
    class Meta:
        verbose_name = 'Formation'
        verbose_name_plural = 'Formations'
        ordering = ['-date_debut']
    
    def __str__(self):
        return f"{self.titre} - {self.date_debut}"
    
    def places_disponibles(self):
        return self.capacite - self.inscriptions.count()

class InscriptionFormation(models.Model):
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('APPROUVEE', 'Approuvée'),
        ('REFUSEE', 'Refusée'),
    ]
    
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='inscriptions_formation', verbose_name='Employé')
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name='inscriptions', verbose_name='Formation')
    date_inscription = models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")
    statut = models.CharField(max_length=15, choices=STATUT_CHOICES, default='EN_ATTENTE', verbose_name='Statut')
    note = models.TextField(blank=True, verbose_name='Note')
    
    class Meta:
        verbose_name = 'Inscription formation'
        verbose_name_plural = 'Inscriptions formations'
        unique_together = ['employe', 'formation']
        ordering = ['-date_inscription']
    
    def __str__(self):
        return f"{self.employe.get_full_name()} - {self.formation.titre}"

class Conge(models.Model):
    TYPE_CHOICES = [
        ('ANNUEL', 'Congé annuel'),
        ('MALADIE', 'Congé maladie'),
        ('MATERNITE', 'Congé maternité'),
        ('PATERNITE', 'Congé paternité'),
        ('SANS_SOLDE', 'Congé sans solde'),
        ('SPECIAL', 'Congé spécial'),
        ('FORMATION', 'Congé formation'),
        ('EXCEPTIONNEL', 'Congé exceptionnel'),
        ('FAMILIAL', 'Congé familial'),
        ('MISSION', 'Congé pour mission'),
        ('SEMINAIRE', 'Congé séminaire'),
        ('ETUDE', 'Congé d\'étude'),
        ('ADMINISTRATIF', 'Congé administratif'),
        ('DEUIL', 'Congé deuil'),
        ('MARIAGE', 'Congé mariage'),
        ('NAISSANCE', 'Congé naissance'),
        ('ACCIDENT', 'Congé accident du travail'),
        ('REPOS', 'Congé de repos compensateur'),
        ('SANTE', 'Congé pour raisons de santé'),
        ('SABBATIQUE', 'Congé sabbatique'),
        ('AUTRE', 'Autre'),
    ]
    
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('APPROUVE', 'Approuvé'),
        ('REFUSE', 'Refusé'),
    ]
    
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='conges', verbose_name='Employé')
    type_conge = models.CharField(max_length=15, choices=TYPE_CHOICES, verbose_name='Type de congé')
    date_debut = models.DateField(verbose_name='Date de début')
    date_fin = models.DateField(verbose_name='Date de fin')
    nombre_jours = models.IntegerField(verbose_name='Nombre de jours', validators=[MinValueValidator(1)])
    motif = models.TextField(verbose_name='Motif')
    statut = models.CharField(max_length=15, choices=STATUT_CHOICES, default='EN_ATTENTE', verbose_name='Statut')
    date_demande = models.DateTimeField(auto_now_add=True, verbose_name='Date de demande')
    date_reponse = models.DateTimeField(blank=True, null=True, verbose_name='Date de réponse')
    commentaire_rh = models.TextField(blank=True, verbose_name='Commentaire RH')
    
    class Meta:
        verbose_name = 'Congé'
        verbose_name_plural = 'Congés'
        ordering = ['-date_demande']
    
    def __str__(self):
        return f"{self.employe.get_full_name()} - {self.get_type_conge_display()} ({self.date_debut})"

class Contrat(models.Model):
    TYPE_CHOICES = [
        ('CDI', 'CDI - Contrat à durée indéterminée'),
        ('CDD', 'CDD - Contrat à durée déterminée'),
        ('VACATAIRE', 'Vacataire'),
        ('PRESTATAIRE', 'Prestataire'),
    ]
    
    STATUT_CHOICES = [
        ('ACTIF', 'Actif'),
        ('EXPIRE', 'Expiré'),
        ('RESILIE', 'Résilié'),
    ]
    
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='contrats', verbose_name='Employé')
    type_contrat = models.CharField(max_length=15, choices=TYPE_CHOICES, verbose_name='Type de contrat')
    date_debut = models.DateField(verbose_name='Date de début')
    date_fin = models.DateField(blank=True, null=True, verbose_name='Date de fin')
    salaire_base = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Salaire de base')
    poste = models.CharField(max_length=100, verbose_name='Poste')
    departement = models.CharField(max_length=100, verbose_name='Département')
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='ACTIF', verbose_name='Statut')
    document = models.FileField(upload_to='contrats/', blank=True, null=True, verbose_name='Document')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    
    class Meta:
        verbose_name = 'Contrat'
        verbose_name_plural = 'Contrats'
        ordering = ['-date_debut']
    
    def __str__(self):
        return f"{self.employe.get_full_name()} - {self.get_type_contrat_display()}"

class Salaire(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='salaires', verbose_name='Employé')
    mois = models.IntegerField(verbose_name='Mois', validators=[MinValueValidator(1), MaxValueValidator(12)])
    annee = models.IntegerField(verbose_name='Année')
    salaire_base = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Salaire de base')
    salaire_net = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Salaire net')
    date_paiement = models.DateField(verbose_name='Date de paiement')
    bulletin = models.FileField(upload_to='bulletins/', blank=True, null=True, verbose_name='Bulletin de paie')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    
    class Meta:
        verbose_name = 'Salaire'
        verbose_name_plural = 'Salaires'
        unique_together = ['employe', 'mois', 'annee']
        ordering = ['-annee', '-mois']
    
    def __str__(self):
        return f"{self.employe.get_full_name()} - {self.mois}/{self.annee}"
    
    def save(self, *args, **kwargs):
        # Le salaire net correspond désormais uniquement au salaire de base
        # (les primes et déductions ont été retirées du modèle)
        self.salaire_net = self.salaire_base
        super().save(*args, **kwargs)

class Presence(models.Model):
    STATUT_CHOICES = [
        ('PRESENT', 'Présent'),
        ('ABSENT', 'Absent'),
        ('RETARD', 'Retard'),
        ('CONGE', 'En congé'),
        ('TELETRAVAIL', 'Télétravail'),
    ]
    
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='presences', verbose_name='Employé')
    date = models.DateField(verbose_name='Date')
    heure_arrivee = models.TimeField(blank=True, null=True, verbose_name="Heure d'arrivée")
    heure_depart = models.TimeField(blank=True, null=True, verbose_name='Heure de départ')
    statut = models.CharField(max_length=15, choices=STATUT_CHOICES, default='PRESENT', verbose_name='Statut')
    note = models.TextField(blank=True, verbose_name='Note')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    
    class Meta:
        verbose_name = 'Présence'
        verbose_name_plural = 'Présences'
        unique_together = ['employe', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.employe.get_full_name()} - {self.date} - {self.get_statut_display()}"

class DossierPersonnel(models.Model):
    TYPE_DOCUMENT_CHOICES = [
        ('CONTRAT', 'Contrat de travail'),
        ('CV', 'CV'),
        ('DIPLOME', 'Diplôme'),
        ('CERTIFICAT', 'Certificat'),
        ('EVALUATION', 'Évaluation'),
        ('SANCTION', 'Sanction'),
        ('AUTRE', 'Autre'),
    ]
    
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='dossiers', verbose_name='Employé')
    type_document = models.CharField(max_length=20, choices=TYPE_DOCUMENT_CHOICES, verbose_name='Type de document')
    titre = models.CharField(max_length=200, verbose_name='Titre du document')
    description = models.TextField(blank=True, verbose_name='Description')
    document = models.FileField(upload_to='dossiers_personnel/', verbose_name='Document')
    date_ajout = models.DateTimeField(auto_now_add=True, verbose_name='Date d\'ajout')
    date_expiration = models.DateField(null=True, blank=True, verbose_name='Date d\'expiration')
    confidentiel = models.BooleanField(default=False, verbose_name='Confidentiel')
    
    class Meta:
        verbose_name = 'Dossier personnel'
        verbose_name_plural = 'Dossiers personnels'
        ordering = ['-date_ajout']
    
    def __str__(self):
        return f"{self.employe.get_full_name()} - {self.titre}"

class JourTravail(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='jours_travail', verbose_name='Employé')
    date = models.DateField(verbose_name='Date')
    heures_travaillees = models.DecimalField(max_digits=4, decimal_places=2, default=8.0, 
                                           verbose_name='Heures travaillées')
    heures_supplementaires = models.DecimalField(max_digits=4, decimal_places=2, default=0, 
                                               verbose_name='Heures supplémentaires')
    commentaire = models.TextField(blank=True, verbose_name='Commentaire')
    valide = models.BooleanField(default=False, verbose_name='Validé')
    
    class Meta:
        verbose_name = 'Jour de travail'
        verbose_name_plural = 'Jours de travail'
        unique_together = ['employe', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.employe.get_full_name()} - {self.date} ({self.heures_travaillees}h)"
