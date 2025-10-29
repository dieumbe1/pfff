#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_rh.settings')
django.setup()

from django.contrib.auth.models import User
from rh_app.models import Employe, Departement
from datetime import date

print("🔧 Correction complète du système d'authentification...")

# 1. Créer un département par défaut
dept, created = Departement.objects.get_or_create(
    nom='Administration',
    defaults={
        'description': 'Administration système',
        'budget_annuel': 1000000
    }
)

# 2. Réinitialiser tous les mots de passe et créer les profils
users_data = [
    ('admin', 'Admin', 'System', 'admin@admin.com', 'RH'),
    ('marie.louise', 'Marie Louise', 'Dhiédiou', 'marie.louise@ecole.sn', 'RH'),
    ('adama.ngom', 'Adama', 'Ngom', 'adama.ngom@ecole.sn', 'EMPLOYE'),
    ('dieumbe.diop', 'Dieumbe', 'Diop', 'dieumbe.diop@ecole.sn', 'EMPLOYE'),
    ('daba.ndour', 'Daba', 'Ndour', 'daba.ndour@ecole.sn', 'EMPLOYE'),
    ('aminata.diop', 'Aminata', 'Diop', 'aminata.diop@ecole.sn', 'EMPLOYE'),
]

for username, prenom, nom, email, role in users_data:
    print(f"\nTraitement de {username}...")
    
    # Créer ou récupérer l'utilisateur
    user, user_created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'first_name': prenom,
            'last_name': nom,
            'is_active': True,
            'is_staff': role == 'RH',
            'is_superuser': username == 'admin'
        }
    )
    
    # Réinitialiser le mot de passe
    user.set_password('password123')
    user.save()
    
    # Créer ou récupérer le profil employé
    try:
        employe = user.employe
        print(f"  ✅ Profil employé existe déjà: {employe}")
    except Employe.DoesNotExist:
        employe = Employe.objects.create(
            user=user,
            matricule=f"EMP{user.id:04d}",
            prenom=prenom,
            nom=nom,
            email=email,
            telephone='0000000000',
            adresse='Non spécifiée',
            date_naissance=date(1980, 1, 1),
            date_embauche=date(2020, 1, 1),
            poste='Administrateur' if role == 'RH' else 'Employé',
            role=role,
            departement=dept,
            statut='ACTIF'
        )
        print(f"  ✅ Profil employé créé: {employe}")

print("\n🎉 Système corrigé!")
print("\n📋 Identifiants de connexion:")
print("  👤 Admin - username: admin, password: password123")
print("  👤 Marie Louise (RH) - username: marie.louise, password: password123")
print("  👤 Adama (Employé) - username: adama.ngom, password: password123")
print("  👤 Dieumbe (Employé) - username: dieumbe.diop, password: password123")
print("  👤 Daba (Employé) - username: daba.ndour, password: password123")
print("  👤 Aminata (Employé) - username: aminata.diop, password: password123")
