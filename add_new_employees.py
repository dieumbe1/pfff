#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_rh.settings')
django.setup()

from django.contrib.auth.models import User
from rh_app.models import Employe, Departement
from datetime import date

print("👥 Ajout des nouveaux employés...")

# Récupérer les départements existants
departements = {
    'RH': Departement.objects.get(nom='Administration'),
    'INFO': Departement.objects.get_or_create(nom='Informatique', defaults={'description': 'Développement', 'budget_annuel': 5000000})[0],
    'COMPTA': Departement.objects.get_or_create(nom='Comptabilité', defaults={'description': 'Gestion financière', 'budget_annuel': 3000000})[0],
    'FORM': Departement.objects.get_or_create(nom='Formation', defaults={'description': 'Pédagogie', 'budget_annuel': 4000000})[0],
    'ADMIN': Departement.objects.get_or_create(nom='Administration', defaults={'description': 'Administration', 'budget_annuel': 2000000})[0],
}

# Nouveaux employés à ajouter
nouveaux_employes = [
    ('omar.sarr', 'Omar', 'Sarr', 'omar.sarr@ecole.sn', 'Développeur Senior', 'INFO'),
    ('aminata.diop2', 'Aminata', 'Diop', 'aminata.diop2@ecole.sn', 'Comptable', 'COMPTA'),
    ('mouhamed.ngom', 'Mouhamed', 'Ngom', 'mouhamed.ngom@ecole.sn', 'Formateur', 'FORM'),
    ('eva.diedhiou', 'Eva', 'Diedhiou', 'eva.diedhiou@ecole.sn', 'Secrétaire', 'ADMIN'),
    ('anta.ndour', 'Anta', 'Ndour', 'anta.ndour@ecole.sn', 'Développeuse', 'INFO'),
    ('malick.sene', 'Malick', 'Sene', 'malick.sene@ecole.sn', 'Assistant RH', 'RH'),
    ('seydou.sow', 'Seydou', 'Sow', 'seydou.sow@ecole.sn', 'Analyste', 'COMPTA'),
]

for username, prenom, nom, email, poste, dept_code in nouveaux_employes:
    print(f"\nCréation de {prenom} {nom}...")
    
    # Vérifier si l'utilisateur existe déjà
    if User.objects.filter(username=username).exists():
        print(f"  ⚠️  {username} existe déjà, passage au suivant")
        continue
    
    # Créer l'utilisateur
    user = User.objects.create_user(
        username=username,
        email=email,
        first_name=prenom,
        last_name=nom,
        password='123',  # Mot de passe simple
        is_active=True,
        is_staff=False
    )
    
    # Créer le profil employé
    employe = Employe.objects.create(
        user=user,
        matricule=f"EMP{user.id:04d}",
        prenom=prenom,
        nom=nom,
        email=email,
        telephone='0000000000',
        adresse='Dakar, Sénégal',
        date_naissance=date(1990, 1, 1),
        date_embauche=date.today(),
        poste=poste,
        role='EMPLOYE',
        departement=departements[dept_code],
        statut='ACTIF'
    )
    
    print(f"  ✅ {prenom} {nom} créé avec succès")
    print(f"     Username: {username}")
    print(f"     Password: 123")
    print(f"     Poste: {poste}")
    print(f"     Département: {departements[dept_code].nom}")

print(f"\n🎉 {len(nouveaux_employes)} nouveaux employés ajoutés!")
print("\n📋 Tous les identifiants de connexion:")
print("  👤 Marie (RH): username=marie, password=123")
print("  👤 Adama (Employé): username=adama, password=123")
print("  👤 Omar (Employé): username=omar.sarr, password=123")
print("  👤 Aminata (Employé): username=aminata.diop2, password=123")
print("  👤 Mouhamed (Employé): username=mouhamed.ngom, password=123")
print("  👤 Eva (Employé): username=eva.diedhiou, password=123")
print("  👤 Anta (Employé): username=anta.ndour, password=123")
print("  👤 Malick (Employé): username=malick.sene, password=123")
print("  👤 Seydou (Employé): username=seydou.sow, password=123")
