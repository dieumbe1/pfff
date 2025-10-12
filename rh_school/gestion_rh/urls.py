from django.urls import path
from . import views

urlpatterns = [
    # Accueil et dashboards
    path('', views.accueil, name='accueil'),
    path('dashboard-rh/', views.responsable_rh, name='dashboard_rh'),
    path('dashboard-employe/', views.employe_dashboard, name='dashboard_employe'),

    # Départements
    path('departements/', views.liste_departements, name='liste_departements'),
    path('departements/ajouter/', views.ajouter_departement, name='ajouter_departement'),
    path('departements/modifier/<int:pk>/', views.modifier_departement, name='modifier_departement'),
    path('departements/supprimer/<int:pk>/', views.supprimer_departement, name='supprimer_departement'),

    # Employés
    path('employes/', views.liste_employes, name='liste_employes'),
    path('employes/ajouter/', views.ajouter_employe, name='ajouter_employe'),
    path('employes/modifier/<int:pk>/', views.modifier_employe, name='modifier_employe'),
    path('employes/supprimer/<int:pk>/', views.supprimer_employe, name='supprimer_employe'),

    # Formations
    path('formations/', views.liste_formations, name='liste_formations'),
    path('formations/ajouter/', views.ajouter_formation, name='ajouter_formation'),
    path('formations/modifier/<int:pk>/', views.modifier_formation, name='modifier_formation'),
    path('formations/supprimer/<int:pk>/', views.supprimer_formation, name='supprimer_formation'),
    path('mes-formations/', views.mes_formations, name='mes_formations'),

    # Congés
    path('conges/', views.liste_conges, name='liste_conges'),
    path('conges/ajouter/', views.ajouter_conge, name='ajouter_conge'),

    # Contrats
    path('contrats/', views.liste_contrats, name='liste_contrats'),
    path('contrats/ajouter/', views.ajouter_contrat, name='ajouter_contrat'),

    # Salaires
    path('salaires/', views.liste_salaires, name='liste_salaires'),
    path('salaires/ajouter/', views.ajouter_salaire, name='ajouter_salaire'),

    # Jours de travail
    path('jours_travail/', views.liste_jours_travail, name='liste_jours_travail'),
    path('jours_travail/ajouter/', views.ajouter_jour_travail, name='ajouter_jour_travail'),
    path('jours_travail/modifier/<int:pk>/', views.modifier_jour_travail, name='modifier_jour_travail'),
    path('jours_travail/supprimer/<int:pk>/', views.supprimer_jour_travail, name='supprimer_jour_travail'),
]
