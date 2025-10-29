#!/usr/bin/env python
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_rh.settings')
django.setup()

from django.contrib.auth.models import User
from rh_app.models import Employe, Departement

# Créer un utilisateur employé
user, created = User.objects.get_or_create(
    username='employe1',
    defaults={
        'email': 'employe1@ecole.sn',
        'first_name': 'Adama',
        'last_name': 'Ngom'
    }
)
if created:
    user.set_password('employe123')
    user.save()
    print("✅ Utilisateur employé créé : employe1 / employe123")

# Créer un département si nécessaire
departement, created = Departement.objects.get_or_create(
    nom='Informatique',
    defaults={
        'description': 'Développement',
        'budget_annuel': 8000000
    }
)

# Créer l'employé
employe, created = Employe.objects.get_or_create(
    user=user,
    defaults={
        'telephone': '77 234 56 78',
        'poste': 'Développeur',
        'departement': departement,
        'salaire_base': 350000,
        'role': 'EMPLOYE',
        'statut': 'ACTIF'
    }
)

if created:
    print("✅ Employé créé avec succès !")
    print(f"📧 Email: {user.email}")
    print(f"👤 Nom: {user.get_full_name()}")
    print(f"🏢 Département: {departement.nom}")
    print(f"💼 Poste: {employe.poste}")
    print(f"🔑 Identifiants: employe1 / employe123")
else:
    print("ℹ️ L'employé existe déjà")

print("\n🚀 Vous pouvez maintenant vous connecter avec :")
print("   Username: employe1")
print("   Password: employe123")
