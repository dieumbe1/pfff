#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_rh.settings')
django.setup()

from django.contrib.auth.models import User
from rh_app.models import Employe

print('📋 TOUS LES EMPLOYÉS ET LEURS MOTS DE PASSE:')
print('=' * 60)

employes = Employe.objects.all().order_by('prenom')

for e in employes:
    print(f'👤 {e.prenom} {e.nom} ({e.poste})')
    print(f'   Username: {e.user.username}')
    print(f'   Password: 123')
    print(f'   Département: {e.departement.nom}')
    print(f'   Rôle: {e.role}')
    print()

print(f'Total: {employes.count()} employés')
