#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_rh.settings')
django.setup()

from rh_app.models import *
from django.contrib.auth.models import User
from datetime import date

# Créer les départements
dept_rh, _ = Departement.objects.get_or_create(nom='Ressources Humaines', defaults={'description': 'Gestion du personnel', 'budget_annuel': 5000000})
dept_info, _ = Departement.objects.get_or_create(nom='Informatique', defaults={'description': 'Développement', 'budget_annuel': 8000000})
dept_compta, _ = Departement.objects.get_or_create(nom='Comptabilité', defaults={'description': 'Gestion financière', 'budget_annuel': 3000000})
dept_formation, _ = Departement.objects.get_or_create(nom='Formation', defaults={'description': 'Pédagogie', 'budget_annuel': 4000000})
dept_admin, _ = Departement.objects.get_or_create(nom='Administration', defaults={'description': 'Administration', 'budget_annuel': 2000000})

print("✅ Départements créés")

# Créer les employés
users_data = [
    ('marie.louise', 'Marie Louise', 'Dhiédiou', 'RH', dept_rh),
    ('adama.ngom', 'Adama', 'Ngom', 'EMPLOYE', dept_info),
    ('dieumbe.diop', 'Dieumbe', 'Diop', 'EMPLOYE', dept_compta),
    ('daba.ndour', 'Daba', 'Ndour', 'EMPLOYE', dept_formation),
    ('aminata.diop', 'Aminata', 'Diop', 'EMPLOYE', dept_admin),
]

for username, prenom, nom, role, dept in users_data:
    user, created = User.objects.get_or_create(username=username, defaults={'email': f'{username}@ecole.sn'})
    if created:
        user.set_password('password123')
        user.save()
    
    employe, created = Employe.objects.get_or_create(
        user=user,
        defaults={
            'prenom': prenom,
            'nom': nom,
            'role': role,
            'departement': dept,
            'date_embauche': date(2024, 1, 1),
            'salaire_base': 300000 if role == 'RH' else 250000
        }
    )
    if created:
        print(f"✅ Employé créé: {prenom} {nom}")

print("✅ Données créées avec succès!")
