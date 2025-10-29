from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('connexion/', views.connexion, name='login'),
    path('inscription/', views.inscription, name='inscription'),
    path('deconnexion/', views.deconnexion, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/rh/', views.dashboard_rh, name='dashboard_rh'),
    path('dashboard/employe/', views.dashboard_employe, name='dashboard_employe'),
    
    # Employés
    path('employes/', views.liste_employes, name='liste_employes'),
    path('employes/ajouter/', views.ajouter_employe, name='ajouter_employe'),
    path('employes/<int:pk>/', views.detail_employe, name='detail_employe'),
    path('employes/<int:pk>/modifier/', views.modifier_employe, name='modifier_employe'),
    path('employes/<int:pk>/supprimer/', views.supprimer_employe, name='supprimer_employe'),
    
    # Formations
    path('formations/', views.liste_formations, name='liste_formations'),
    path('formations/ajouter/', views.ajouter_formation, name='ajouter_formation'),
    path('formations/<int:pk>/', views.detail_formation, name='detail_formation'),
    path('formations/<int:pk>/modifier/', views.modifier_formation, name='modifier_formation'),
    path('formations/<int:pk>/supprimer/', views.supprimer_formation, name='supprimer_formation'),
    path('formations/<int:pk>/inscrire/', views.inscrire_formation, name='inscrire_formation'),
    
    # Congés
    path('conges/', views.liste_conges, name='liste_conges'),
    path('conges/demander/', views.demander_conge, name='demander_conge'),
    path('conges/<int:pk>/traiter/', views.traiter_conge, name='traiter_conge'),
    
    # Contrats
    path('contrats/', views.liste_contrats, name='liste_contrats'),
    path('contrats/ajouter/', views.ajouter_contrat, name='ajouter_contrat'),
    path('contrats/<int:pk>/', views.detail_contrat, name='detail_contrat'),
    path('contrats/<int:pk>/modifier/', views.modifier_contrat, name='modifier_contrat'),
    path('contrats/<int:pk>/supprimer/', views.supprimer_contrat, name='supprimer_contrat'),
    
    # Salaires
    path('salaires/', views.liste_salaires, name='liste_salaires'),
    path('salaires/ajouter/', views.ajouter_salaire, name='ajouter_salaire'),
    
    # Présences
    path('presences/', views.liste_presences, name='liste_presences'),
    path('presences/ajouter/', views.ajouter_presence, name='ajouter_presence'),
    
    # Départements - CORRIGÉ (URL detail_departement ajoutée)
    path('departements/', views.liste_departements, name='liste_departements'),
    path('departements/ajouter/', views.ajouter_departement, name='ajouter_departement'),
    path('departements/<int:pk>/', views.detail_departement, name='detail_departement'),  # ← LIGNE AJOUTÉE
    path('departements/<int:pk>/modifier/', views.modifier_departement, name='modifier_departement'),
    path('departements/<int:pk>/supprimer/', views.supprimer_departement, name='supprimer_departement'),
    
    # Dossiers personnels
    path('dossiers/', views.liste_dossiers_personnel, name='liste_dossiers_personnel'),
    path('dossiers/ajouter/', views.ajouter_dossier_personnel, name='ajouter_dossier_personnel'),
    path('dossiers/<int:pk>/supprimer/', views.supprimer_dossier_personnel, name='supprimer_dossier_personnel'),
    
    # Jours de travail
    path('jours-travail/', views.liste_jours_travail, name='liste_jours_travail'),
    path('jours-travail/ajouter/', views.ajouter_jour_travail, name='ajouter_jour_travail'),
    path('jours-travail/<int:pk>/supprimer/', views.supprimer_jour_travail, name='supprimer_jour_travail'),
]