from django.contrib import admin
from .models import (
    Departement,
    Employe,
    Formation,
    Contrat,
    Conge,
    Salaire,
    JourDeTravail,
    ProfilUtilisateur
)


# =======================
# ADMIN - DÉPARTEMENT
# =======================
@admin.register(Departement)
class DepartementAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'date_fin')
    search_fields = ('nom', 'description')
    list_filter = ('date_fin',)


# =======================
# ADMIN - EMPLOYÉ
# =======================
@admin.register(Employe)
class EmployeAdmin(admin.ModelAdmin):
    list_display = ('matricule', 'nom', 'prenom', 'email', 'departement', 'date_embauche')
    search_fields = ('matricule', 'nom', 'prenom', 'email')
    list_filter = ('departement', 'sexe')
    raw_id_fields = ('user',)  # utile si tu as beaucoup d'utilisateurs


# =======================
# ADMIN - FORMATION
# =======================
@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ('intitule_formation', 'organisme', 'date_formation', 'cout')
    search_fields = ('intitule_formation', 'organisme')
    list_filter = ('date_formation',)
    filter_horizontal = ('personnel_suivi',)  # meilleure UX pour ManyToMany


# =======================
# ADMIN - CONTRAT
# =======================
@admin.register(Contrat)
class ContratAdmin(admin.ModelAdmin):
    list_display = ('type_contrat', 'employe', 'date_debut', 'date_fin')
    search_fields = ('employe__matricule', 'employe__nom', 'employe__prenom')
    list_filter = ('type_contrat',)
    raw_id_fields = ('employe',)


# =======================
# ADMIN - CONGÉ
# =======================
@admin.register(Conge)
class CongeAdmin(admin.ModelAdmin):
    list_display = ('employe', 'date_debut', 'date_fin', 'motif', 'statut', 'date_demande')
    search_fields = ('employe__nom', 'employe__prenom', 'motif')
    list_filter = ('statut',)
    raw_id_fields = ('employe',)


# =======================
# ADMIN - SALAIRE
# =======================
@admin.register(Salaire)
class SalaireAdmin(admin.ModelAdmin):
    list_display = ('employe', 'montant_base', 'montant_net', 'periode', 'date_effective')
    search_fields = ('employe__nom', 'employe__prenom', 'employe__matricule')
    list_filter = ('periode',)
    raw_id_fields = ('employe',)


# =======================
# ADMIN - JOUR DE TRAVAIL
# =======================
@admin.register(JourDeTravail)
class JourDeTravailAdmin(admin.ModelAdmin):
    list_display = ('jour', 'heure_debut', 'heure_fin', 'statut')
    search_fields = ('jour',)
    filter_horizontal = ('employes',)


# =======================
# ADMIN - PROFIL UTILISATEUR
# =======================
@admin.register(ProfilUtilisateur)
class ProfilUtilisateurAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__username', 'role')
