import os
import django
from datetime import date, timedelta
from decimal import Decimal

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_rh.settings')
django.setup()

from django.contrib.auth.models import User
from rh_app.models import Employe, Departement, Formation, Contrat, Salaire, Presence, Conge, DossierPersonnel, JourTravail

def create_departements():
    """Créer les départements de base"""
    departements = [
        {'nom': 'Ressources Humaines', 'description': 'Gestion du personnel', 'budget_annuel': 5000000},
        {'nom': 'Informatique', 'description': 'Développement et maintenance informatique', 'budget_annuel': 8000000},
        {'nom': 'Comptabilité', 'description': 'Gestion financière et comptable', 'budget_annuel': 3000000},
        {'nom': 'Formation', 'description': 'Pédagogie et formation', 'budget_annuel': 4000000},
        {'nom': 'Administration', 'description': 'Administration générale', 'budget_annuel': 2000000},
    ]

    for dept_data in departements:
        dept, created = Departement.objects.get_or_create(
            nom=dept_data['nom'],
            defaults=dept_data
        )
        if created:
            print(f"Département créé: {dept.nom}")

def create_users_and_employees():
    """Créer les utilisateurs et employés de base"""
    employees_data = [
        {
            'username': 'marie.louise',
            'email': 'marie.louise@ecole.sn',
            'first_name': 'Marie Louise',
            'last_name': 'Dhiédiou',
            'matricule': 'EMP001',
            'role': 'RH',
            'poste': 'Responsable RH',
            'departement_nom': 'Ressources Humaines',
            'salaire_base': 450000,
            'date_embauche': date(2020, 1, 15),
        },
        {
            'username': 'adama.ngom',
            'email': 'adama.ngom@ecole.sn',
            'first_name': 'Adama',
            'last_name': 'Ngom',
            'matricule': 'EMP002',
            'role': 'EMPLOYE',
            'poste': 'Développeur',
            'departement_nom': 'Informatique',
            'salaire_base': 350000,
            'date_embauche': date(2021, 3, 10),
        },
        {
            'username': 'dieumbe.diop',
            'email': 'dieumbe.diop@ecole.sn',
            'first_name': 'Dieumbe',
            'last_name': 'Diop',
            'matricule': 'EMP003',
            'role': 'EMPLOYE',
            'poste': 'Comptable',
            'departement_nom': 'Comptabilité',
            'salaire_base': 320000,
            'date_embauche': date(2021, 6, 1),
        },
        {
            'username': 'daba.ndour',
            'email': 'daba.ndour@ecole.sn',
            'first_name': 'Daba',
            'last_name': 'Ndour',
            'matricule': 'EMP004',
            'role': 'EMPLOYE',
            'poste': 'Formateur',
            'departement_nom': 'Formation',
            'salaire_base': 300000,
            'date_embauche': date(2022, 2, 14),
        },
        {
            'username': 'aminata.diop',
            'email': 'aminata.diop@ecole.sn',
            'first_name': 'Aminata',
            'last_name': 'Diop',
            'matricule': 'EMP005',
            'role': 'EMPLOYE',
            'poste': 'Secrétaire',
            'departement_nom': 'Administration',
            'salaire_base': 280000,
            'date_embauche': date(2020, 8, 20),
        },
    ]

    for emp_data in employees_data:
        # Créer l'utilisateur
        user, user_created = User.objects.get_or_create(
            username=emp_data['username'],
            defaults={
                'email': emp_data['email'],
                'first_name': emp_data['first_name'],
                'last_name': emp_data['last_name'],
                'password': 'isep'  # Mot de passe demandé
            }
        )

        # Récupérer le département
        try:
            departement = Departement.objects.get(nom=emp_data['departement_nom'])
        except Departement.DoesNotExist:
            print(f"Département {emp_data['departement_nom']} non trouvé, création...")
            departement = Departement.objects.create(
                nom=emp_data['departement_nom'],
                description=f"Département {emp_data['departement_nom']}",
                budget_annuel=1000000
            )

        # Créer l'employé
        employe, emp_created = Employe.objects.get_or_create(
            user=user,
            defaults={
                'matricule': emp_data['matricule'],
                'role': emp_data['role'],
                'nom': emp_data['last_name'],
                'prenom': emp_data['first_name'],
                'email': emp_data['email'],
                'telephone': '77 123 45 67',
                'adresse': 'Dakar, Sénégal',
                'date_naissance': date(1990, 1, 1),
                'date_embauche': emp_data['date_embauche'],
                'poste': emp_data['poste'],
                'departement': departement,
            }
        )

        if emp_created:
            print(f"Employé créé: {employe.get_full_name()}")

            # Créer le contrat
            contrat = Contrat.objects.create(
                employe=employe,
                type_contrat='CDI',
                date_debut=emp_data['date_embauche'],
                salaire_base=Decimal(str(emp_data['salaire_base'])),
                poste=emp_data['poste'],
                departement=departement.nom,
                statut='ACTIF'
            )
            print(f"Contrat créé pour {employe.get_full_name()}")

def create_formations():
    """Créer des formations de base"""
    formations_data = [
        {
            'titre': 'Formation Django Avancé',
            'description': 'Maîtrise des concepts avancés de Django',
            'date_debut': date(2024, 12, 15),
            'date_fin': date(2024, 12, 18),
            'lieu': 'Salle de formation A',
            'formateur': 'Marie Martin',
            'capacite': 15,
            'statut': 'PROGRAMMEE',
        },
        {
            'titre': 'Gestion de Projet Agile',
            'description': 'Méthodologies agiles pour la gestion de projet',
            'date_debut': date(2024, 12, 30),
            'date_fin': date(2024, 12, 31),
            'lieu': 'Salle de conférence B',
            'formateur': 'Pierre Durand',
            'capacite': 20,
            'statut': 'PROGRAMMEE',
        },
        {
            'titre': 'Communication Interpersonnelle',
            'description': 'Développer ses compétences en communication',
            'date_debut': date(2025, 1, 15),
            'date_fin': date(2025, 1, 16),
            'lieu': 'Salle de formation C',
            'formateur': 'Fatou Sall',
            'capacite': 12,
            'statut': 'PROGRAMMEE',
        },
    ]

    for form_data in formations_data:
        formation, created = Formation.objects.get_or_create(
            titre=form_data['titre'],
            date_debut=form_data['date_debut'],
            defaults=form_data
        )
        if created:
            print(f"Formation créée: {formation.titre}")

def create_presences():
    """Créer des présences pour les employés"""
    employees = Employe.objects.all()
    today = date.today()

    for employe in employees:
        for i in range(30):  # 30 jours de présence
            presence_date = today - timedelta(days=i)
            Presence.objects.get_or_create(
                employe=employe,
                date=presence_date,
                defaults={
                    'heure_arrivee': '08:00:00',
                    'heure_depart': '17:00:00',
                    'statut': 'PRESENT',
                }
            )
    print("Présences créées pour tous les employés")

def create_salaires():
    """Créer des salaires pour les employés"""
    employees = Employe.objects.all()
    current_date = date.today()

    for employe in employees:
        # Salaire du mois en cours
        Salaire.objects.get_or_create(
            employe=employe,
            mois=current_date.month,
            annee=current_date.year,
            defaults={
                'salaire_base': employe.contrats.first().salaire_base if employe.contrats.exists() else 300000,
                'date_paiement': current_date,
            }
        )
    print("Salaires créés pour tous les employés")

def main():
    """Fonction principale pour créer toutes les données"""
    print("Début de la création des données...")

    try:
        create_departements()
        create_users_and_employees()
        create_formations()
        create_presences()
        create_salaires()

        print("\nToutes les données ont été créées avec succès!")
        print("\nComptes utilisateurs créés:")
        print("- marie.louise / isep (RH)")
        print("- adama.ngom / isep (Employé)")
        print("- dieumbe.diop / isep (Employé)")
        print("- daba.ndour / isep (Employé)")
        print("- aminata.diop / isep (Employé)")

    except Exception as e:
        print(f"Erreur lors de la création des données: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
