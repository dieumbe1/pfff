#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_rh.settings')
django.setup()

from django.contrib.auth.models import User
from rh_app.models import Employe, Departement
from datetime import date

# Récupérer ou créer un département
dept, created = Departement.objects.get_or_create(
    nom='Administration',
    defaults={
        'description': 'Administration système',
        'budget_annuel': 1000000
    }
)

# Récupérer tous les superutilisateurs
admin_users = User.objects.filter(is_superuser=True)

print(f"Trouvé {admin_users.count()} superutilisateur(s)")

for admin_user in admin_users:
    print(f"Traitement de l'utilisateur: {admin_user.username}")
    
    # Vérifier si un profil employé existe déjà
    try:
        employe = admin_user.employe
        print(f"  ✅ Profil employé existe déjà: {employe}")
    except Employe.DoesNotExist:
        # Créer un profil employé pour l'admin
        employe = Employe.objects.create(
            user=admin_user,
            matricule=f"ADMIN{admin_user.id:03d}",
            prenom=admin_user.first_name or 'Admin',
            nom=admin_user.last_name or 'System',
            email=admin_user.email or f'{admin_user.username}@admin.local',
            telephone='0000000000',
            adresse='Système',
            date_naissance=date(1980, 1, 1),
            date_embauche=date(2020, 1, 1),
            poste='Administrateur',
            role='RH',
            departement=dept,
            statut='ACTIF'
        )
        print(f"  ✅ Profil employé créé: {employe}")

print("✅ Tous les superutilisateurs ont maintenant un profil employé!")
