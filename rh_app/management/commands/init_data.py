from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rh_app.models import Employe, Formation, Conge, Contrat, Salaire, Presence
from datetime import date, timedelta, time
from decimal import Decimal

class Command(BaseCommand):
    help = 'Initialise les données de test pour l\'application RH'

    def handle(self, *args, **options):
        self.stdout.write('Création des utilisateurs de test...')
        
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@rh.com',
                password='admin123',
                first_name='Admin',
                last_name='RH'
            )
            
            Employe.objects.create(
                user=admin_user,
                matricule='RH001',
                role='RH',
                nom='RH',
                prenom='Admin',
                email='admin@rh.com',
                telephone='0123456789',
                adresse='1 rue de la RH, 75001 Paris',
                date_naissance=date(1985, 5, 15),
                date_embauche=date(2020, 1, 1),
                poste='Responsable RH',
                departement='Ressources Humaines',
                statut='ACTIF'
            )
            self.stdout.write(self.style.SUCCESS('✓ Admin RH créé (username: admin, password: admin123)'))
        
        if not User.objects.filter(username='employe1').exists():
            emp_user = User.objects.create_user(
                username='employe1',
                email='jean.dupont@ecole.com',
                password='employe123',
                first_name='Jean',
                last_name='Dupont'
            )
            
            employe = Employe.objects.create(
                user=emp_user,
                matricule='EMP001',
                role='EMPLOYE',
                nom='Dupont',
                prenom='Jean',
                email='jean.dupont@ecole.com',
                telephone='0612345678',
                adresse='10 avenue des Champs, 75008 Paris',
                date_naissance=date(1990, 3, 20),
                date_embauche=date(2022, 6, 1),
                poste='Développeur',
                departement='Informatique',
                statut='ACTIF'
            )
            self.stdout.write(self.style.SUCCESS('✓ Employé créé (username: employe1, password: employe123)'))
            
            Contrat.objects.create(
                employe=employe,
                type_contrat='CDI',
                date_debut=date(2022, 6, 1),
                salaire_base=Decimal('3500.00'),
                poste='Développeur',
                departement='Informatique',
                statut='ACTIF'
            )
            
            Salaire.objects.create(
                employe=employe,
                mois=10,
                annee=2025,
                salaire_base=Decimal('3500.00'),
                salaire_net=Decimal('3500.00'),
                date_paiement=date(2025, 10, 30)
            )
        
        if Formation.objects.count() == 0:
            Formation.objects.create(
                titre='Formation Django Avancé',
                description='Apprenez les concepts avancés de Django pour développer des applications web robustes.',
                date_debut=date.today() + timedelta(days=30),
                date_fin=date.today() + timedelta(days=33),
                lieu='Salle de formation A',
                formateur='Marie Martin',
                capacite=15,
                statut='PROGRAMMEE'
            )
            
            Formation.objects.create(
                titre='Gestion de Projet Agile',
                description='Maîtrisez les méthodologies Agile et Scrum pour gérer vos projets efficacement.',
                date_debut=date.today() + timedelta(days=45),
                date_fin=date.today() + timedelta(days=46),
                lieu='Salle de conférence B',
                formateur='Pierre Durand',
                capacite=20,
                statut='PROGRAMMEE'
            )
            self.stdout.write(self.style.SUCCESS('✓ Formations de test créées'))
        
        self.stdout.write(self.style.SUCCESS('Initialisation terminée avec succès!'))
        self.stdout.write(self.style.WARNING('\nInformations de connexion:'))
        self.stdout.write('  Responsable RH - username: admin, password: admin123')
        self.stdout.write('  Employé - username: employe1, password: employe123')
