#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_rh.settings')
django.setup()

from django.contrib.auth.models import User
from rh_app.models import Employe, Departement
from datetime import date

# Récupérer ou créer un département par défaut
dept, created = Departement.objects.get_or_create(
    nom='Administration',
    defaults={
        'description': 'Administration système',
        'budget_annuel': 1000000
    }
)

print("🔧 Création des profils employés pour tous les utilisateurs...")

# Récupérer tous les utilisateurs
users = User.objects.all()
print(f"Trouvé {users.count()} utilisateur(s)")

for user in users:
    print(f"\nTraitement de l'utilisateur: {user.username}")
    
    # Vérifier si un profil employé existe déjà
    try:
        employe = user.employe
        print(f"  ✅ Profil employé existe déjà: {employe}")
    except Employe.DoesNotExist:
        # Déterminer le rôle basé sur les permissions
        role = 'RH' if user.is_superuser or user.is_staff else 'EMPLOYE'
        
        # Créer un profil employé
        employe = Employe.objects.create(
            user=user,
            matricule=f"EMP{user.id:04d}",
            prenom=user.first_name or 'Utilisateur',
            nom=user.last_name or 'Système',
            email=user.email or f'{user.username}@local.local',
            telephone='0000000000',
            adresse='Non spécifiée',
            date_naissance=date(1980, 1, 1),
            date_embauche=date(2020, 1, 1),
            poste='Employé' if role == 'EMPLOYE' else 'Administrateur',
            role=role,
            departement=dept,
            statut='ACTIF'
        )
        print(f"  ✅ Profil employé créé: {employe} (Rôle: {role})")

print("\n🎉 Tous les utilisateurs ont maintenant un profil employé!")
print("\n📋 Informations de connexion:")
print("  👤 Admin - username: admin, password: admin")
print("  👤 Marie Louise (RH) - username: marie.louise, password: password123")
print("  👤 Adama (Employé) - username: adama.ngom, password: password123")
print("  👤 Dieumbe (Employé) - username: dieumbe.diop, password: password123")
print("  👤 Daba (Employé) - username: daba.ndour, password: password123")
print("  👤 Aminata (Employé) - username: aminata.diop, password: password123")
