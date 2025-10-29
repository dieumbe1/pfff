#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_rh.settings')
django.setup()

from django.contrib.auth.models import User
from rh_app.models import Employe, Departement
from datetime import date

print("🔧 Résolution définitive du problème d'authentification...")

# 1. Supprimer tous les utilisateurs existants (sauf admin)
print("Suppression des anciens utilisateurs...")
User.objects.exclude(username='admin').delete()
Employe.objects.all().delete()

# 2. Créer un département par défaut
dept, created = Departement.objects.get_or_create(
    nom='Administration',
    defaults={
        'description': 'Administration système',
        'budget_annuel': 1000000
    }
)

# 3. Créer les utilisateurs un par un avec vérification
users_data = [
    ('marie.louise', 'Marie Louise', 'Dhiédiou', 'marie.louise@ecole.sn', 'RH', 'Responsable RH'),
    ('adama.ngom', 'Adama', 'Ngom', 'adama.ngom@ecole.sn', 'EMPLOYE', 'Développeur'),
    ('dieumbe.diop', 'Dieumbe', 'Diop', 'dieumbe.diop@ecole.sn', 'EMPLOYE', 'Comptable'),
    ('daba.ndour', 'Daba', 'Ndour', 'daba.ndour@ecole.sn', 'EMPLOYE', 'Formateur'),
    ('aminata.diop', 'Aminata', 'Diop', 'aminata.diop@ecole.sn', 'EMPLOYE', 'Secrétaire'),
]

for username, prenom, nom, email, role, poste in users_data:
    print(f"\nCréation de {username}...")
    
    # Créer l'utilisateur
    user = User.objects.create_user(
        username=username,
        email=email,
        first_name=prenom,
        last_name=nom,
        password='password123',  # Utiliser create_user avec password directement
        is_active=True,
        is_staff=(role == 'RH'),
        is_superuser=False
    )
    
    # Vérifier que le mot de passe est correct
    if user.check_password('password123'):
        print(f"  ✅ Mot de passe vérifié pour {username}")
    else:
        print(f"  ❌ Problème de mot de passe pour {username}")
        user.set_password('password123')
        user.save()
    
    # Créer le profil employé
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
        poste=poste,
        role=role,
        departement=dept,
        statut='ACTIF'
    )
    
    print(f"  ✅ Utilisateur et profil créés: {username}")

# 4. Vérification finale
print("\n🔍 Vérification finale...")
for user in User.objects.all():
    if user.check_password('password123'):
        print(f"✅ {user.username} - Connexion OK")
    else:
        print(f"❌ {user.username} - Problème de connexion")

print("\n🎉 Système prêt!")
print("\n📋 Testez maintenant avec:")
print("  Username: marie.louise, Password: password123")
print("  Username: adama.ngom, Password: password123")
