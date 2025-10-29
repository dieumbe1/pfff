#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_rh.settings')
django.setup()

from rh_app.models import Employe, Departement

print("🔧 Correction des postes et départements...")

# Créer les vrais départements
departements = {
    'RH': Departement.objects.get_or_create(nom='Ressources Humaines', defaults={'description': 'Gestion du personnel', 'budget_annuel': 5000000})[0],
    'INFO': Departement.objects.get_or_create(nom='Informatique', defaults={'description': 'Développement', 'budget_annuel': 8000000})[0],
    'COMPTA': Departement.objects.get_or_create(nom='Comptabilité', defaults={'description': 'Gestion financière', 'budget_annuel': 3000000})[0],
    'FORM': Departement.objects.get_or_create(nom='Formation', defaults={'description': 'Pédagogie', 'budget_annuel': 4000000})[0],
    'ADMIN': Departement.objects.get_or_create(nom='Administration', defaults={'description': 'Administration', 'budget_annuel': 2000000})[0],
}

# Corrections des employés
corrections = [
    ('marie', 'Responsable RH', 'RH'),
    ('adama', 'Développeur', 'INFO'),
    ('daba', 'Formateur', 'FORM'),
    ('dieumbe', 'Comptable', 'COMPTA'),
    ('aminata.diop2', 'Comptable', 'COMPTA'),
    ('omar.sarr', 'Développeur Senior', 'INFO'),
    ('mouhamed.ngom', 'Formateur', 'FORM'),
    ('eva.diedhiou', 'Secrétaire', 'ADMIN'),
    ('anta.ndour', 'Développeuse', 'INFO'),
    ('malick.sene', 'Assistant RH', 'RH'),
    ('seydou.sow', 'Analyste', 'COMPTA'),
]

for username, nouveau_poste, nouveau_dept in corrections:
    try:
        employe = Employe.objects.get(user__username=username)
        ancien_poste = employe.poste
        ancien_dept = employe.departement.nom
        
        employe.poste = nouveau_poste
        employe.departement = departements[nouveau_dept]
        employe.save()
        
        print(f"✅ {employe.prenom} {employe.nom}")
        print(f"   Poste: {ancien_poste} → {nouveau_poste}")
        print(f"   Département: {ancien_dept} → {departements[nouveau_dept].nom}")
        print()
        
    except Employe.DoesNotExist:
        print(f"❌ Employé {username} non trouvé")

print("🎉 Corrections terminées!")
