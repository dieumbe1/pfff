#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_rh.settings')
django.setup()

from django.contrib.auth.models import User
from rh_app.models import Employe, Departement
from datetime import date

print("🔧 Création d'un système de connexion simple...")

# Supprimer tout et recommencer proprement
User.objects.all().delete()
Employe.objects.all().delete()
Departement.objects.all().delete()

# Créer un département
dept = Departement.objects.create(
    nom='Administration',
    description='Administration générale',
    budget_annuel=1000000
)

# Créer les utilisateurs SIMPLES
users_simples = [
    ('marie', 'Marie', 'Louise', 'RH'),
    ('adama', 'Adama', 'Ngom', 'EMPLOYE'),
    ('dieumbe', 'Dieumbe', 'Diop', 'EMPLOYE'),
    ('daba', 'Daba', 'Ndour', 'EMPLOYE'),
    ('aminata', 'Aminata', 'Diop', 'EMPLOYE'),
]

for username, prenom, nom, role in users_simples:
    print(f"Création de {username}...")
    
    # Créer utilisateur avec mot de passe simple
    user = User.objects.create_user(
        username=username,
        password='123',  # Mot de passe simple
        first_name=prenom,
        last_name=nom,
        email=f'{username}@test.com',
        is_active=True,
        is_staff=(role == 'RH')
    )
    
    # Créer profil employé
    Employe.objects.create(
        user=user,
        matricule=f"EMP{user.id:03d}",
        prenom=prenom,
        nom=nom,
        email=f'{username}@test.com',
        telephone='0000000000',
        adresse='Test',
        date_naissance=date(1990, 1, 1),
        date_embauche=date(2020, 1, 1),
        poste='Test',
        role=role,
        departement=dept,
        statut='ACTIF'
    )
    
    print(f"  ✅ {username} créé avec succès")

print("\n🎉 Système simple créé!")
print("\n📋 Connexion SIMPLE:")
print("  👤 Marie (RH): username=marie, password=123")
print("  👤 Adama (Employé): username=adama, password=123")
print("  👤 Dieumbe (Employé): username=dieumbe, password=123")
print("  👤 Daba (Employé): username=daba, password=123")
print("  👤 Aminata (Employé): username=aminata, password=123")
