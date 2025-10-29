from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Employe, Formation, InscriptionFormation, Conge, Contrat, Salaire, Presence, Departement, DossierPersonnel, JourTravail
from .forms import (
    EmployeSignupForm, LoginForm, EmployeForm, FormationForm, CongeForm, 
    ContratForm, SalaireForm, PresenceForm, InscriptionFormationForm,
    DepartementForm, DossierPersonnelForm, JourTravailForm
)

def accueil(request):
    return render(request, 'rh_app/accueil.html')

def connexion(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Debug: afficher les valeurs
            print(f"Tentative de connexion: username='{username}', password='{password}'")
            
            user = authenticate(request, username=username, password=password)
            print(f"Résultat authenticate: {user}")
            
            if user is not None:
                print(f"Utilisateur trouvé: {user.username}, actif: {user.is_active}")
                login(request, user)
                return redirect('dashboard')
            else:
                # Vérifier si l'utilisateur existe
                try:
                    user_exists = User.objects.get(username=username)
                    print(f"Utilisateur existe: {user_exists.username}, actif: {user_exists.is_active}")
                    # Tester le mot de passe
                    if user_exists.check_password(password):
                        print("Mot de passe correct!")
                        login(request, user_exists)
                        return redirect('dashboard')
                    else:
                        print("Mot de passe incorrect!")
                except User.DoesNotExist:
                    print(f"Utilisateur {username} n'existe pas")
                
                messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    else:
        form = LoginForm()
    return render(request, 'rh_app/connexion.html', {'form': form})

@login_required
def deconnexion(request):
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('accueil')

@login_required
def dashboard(request):
    try:
        employe = request.user.employe
        if employe.role == 'RH':
            return redirect('dashboard_rh')
        else:
            return redirect('dashboard_employe')
    except Employe.DoesNotExist:
        messages.error(request, 'Profil employé non trouvé.')
        return redirect('accueil')

@login_required
def dashboard_rh(request):
    try:
        employe = request.user.employe
        if employe.role != 'RH':
            messages.error(request, 'Accès non autorisé.')
            return redirect('dashboard_employe')
        
        # Récupérer les vraies données de la base
        total_employes = Employe.objects.count()
        conges_en_attente = Conge.objects.filter(statut='EN_ATTENTE').count()
        total_formations = Formation.objects.count()
        total_departements = Departement.objects.count()
        employes_recents = Employe.objects.order_by('-date_embauche')[:5]
        
        contrats_actifs_count = Contrat.objects.filter(statut='ACTIF').count()
        contrats_expirant_count = Contrat.objects.filter(
            statut='ACTIF',
            date_fin__lte=timezone.now().date() + timedelta(days=30)
        ).count()
        contrats_expires_count = Contrat.objects.filter(statut='EXPIRE').count()
        
        context = {
            'employe': employe,
            'total_employes': total_employes,
            'conges_en_attente': conges_en_attente,
            'total_formations': total_formations,
            'total_departements': total_departements,
            'employes_recents': employes_recents,
            'contrats_actifs_count': contrats_actifs_count,
            'contrats_expirant_count': contrats_expirant_count,
            'contrats_expires_count': contrats_expires_count,
        }
        return render(request, 'rh_app/dashboard_rh.html', context)
    except Employe.DoesNotExist:
        messages.error(request, 'Profil employé non trouvé.')
        return redirect('accueil')

@login_required
def dashboard_employe(request):
    employe = request.user.employe
    
    mes_conges = Conge.objects.filter(employe=employe).order_by('-date_demande')[:5]
    mes_formations = InscriptionFormation.objects.filter(employe=employe).order_by('-date_inscription')[:5]
    mes_presences = Presence.objects.filter(employe=employe).order_by('-date')[:10]
    mon_dernier_salaire = Salaire.objects.filter(employe=employe).first()
    
    context = {
        'employe': employe,
        'mes_conges': mes_conges,
        'mes_formations': mes_formations,
        'mes_presences': mes_presences,
        'mon_dernier_salaire': mon_dernier_salaire,
    }
    return render(request, 'rh_app/dashboard_employe.html', context)

@login_required
def liste_employes(request):
    employe = request.user.employe
    if employe.role != 'RH':
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')
    
    # Récupérer les vrais employés de la base de données
    employes = Employe.objects.all().order_by('nom', 'prenom')
    context = {'employes': employes}
    return render(request, 'rh_app/employes/liste.html', context)

@login_required
def ajouter_employe(request):
    employe = request.user.employe
    if employe.role != 'RH':
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = EmployeForm(request.POST, request.FILES)
        if form.is_valid():
            employe_obj = form.save(commit=False)
            user = User.objects.create_user(
                username=form.cleaned_data['matricule'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['prenom'],
                last_name=form.cleaned_data['nom'],
                password='motdepasse123'
            )
            employe_obj.user = user
            employe_obj.save()
            messages.success(request, f'Employé {employe_obj.get_full_name()} ajouté avec succès.')
            return redirect('liste_employes')
    else:
        form = EmployeForm()
    
    return render(request, 'rh_app/employes/form.html', {'form': form, 'action': 'Ajouter'})

@login_required
def modifier_employe(request, pk):
    employe = request.user.employe
    if employe.role != 'RH':
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')
    
    employe_obj = get_object_or_404(Employe, pk=pk)
    
    if request.method == 'POST':
        form = EmployeForm(request.POST, request.FILES, instance=employe_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'Employé {employe_obj.get_full_name()} modifié avec succès.')
            return redirect('liste_employes')
    else:
        form = EmployeForm(instance=employe_obj)
    
    return render(request, 'rh_app/employes/form.html', {'form': form, 'action': 'Modifier'})

@login_required
def detail_employe(request, pk):
    employe = request.user.employe
    employe_obj = get_object_or_404(Employe, pk=pk)
    
    if employe.role != 'RH' and employe != employe_obj:
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')
    
    contrats = employe_obj.contrats.all()
    conges = employe_obj.conges.all()
    salaires = employe_obj.salaires.all()[:6]
    
    context = {
        'employe_obj': employe_obj,
        'contrats': contrats,
        'conges': conges,
        'salaires': salaires,
    }
    return render(request, 'rh_app/employes/detail.html', context)

@login_required
def liste_formations(request):
    formations = Formation.objects.all().order_by('-date_debut')
    context = {'formations': formations}
    return render(request, 'rh_app/formations/liste.html', context)

@login_required
def ajouter_formation(request):
    employe = request.user.employe
    if employe.role != 'RH':
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = FormationForm(request.POST)
        if form.is_valid():
            formation = form.save()
            messages.success(request, f'Formation "{formation.titre}" ajoutée avec succès.')
            return redirect('liste_formations')
    else:
        form = FormationForm()
    
    return render(request, 'rh_app/formations/form.html', {'form': form, 'action': 'Ajouter'})

@login_required
def modifier_formation(request, pk):
    employe = request.user.employe
    if employe.role != 'RH':
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')
    
    formation = get_object_or_404(Formation, pk=pk)
    
    if request.method == 'POST':
        form = FormationForm(request.POST, instance=formation)
        if form.is_valid():
            form.save()
            messages.success(request, f'Formation "{formation.titre}" modifiée avec succès.')
            return redirect('liste_formations')
    else:
        form = FormationForm(instance=formation)
    
    return render(request, 'rh_app/formations/form.html', {'form': form, 'action': 'Modifier'})

@login_required
def detail_formation(request, pk):
    formation = get_object_or_404(Formation, pk=pk)
    inscriptions = formation.inscriptions.all()
    
    employe = request.user.employe
    est_inscrit = InscriptionFormation.objects.filter(employe=employe, formation=formation).exists()
    
    context = {
        'formation': formation,
        'inscriptions': inscriptions,
        'est_inscrit': est_inscrit,
        'places_disponibles': formation.places_disponibles(),
    }
    return render(request, 'rh_app/formations/detail.html', context)

@login_required
def inscrire_formation(request, pk):
    formation = get_object_or_404(Formation, pk=pk)
    employe = request.user.employe
    
    if InscriptionFormation.objects.filter(employe=employe, formation=formation).exists():
        messages.warning(request, 'Vous êtes déjà inscrit à cette formation.')
    elif formation.places_disponibles() <= 0:
        messages.error(request, 'Cette formation est complète.')
    else:
        InscriptionFormation.objects.create(employe=employe, formation=formation)
        messages.success(request, f'Inscription à la formation "{formation.titre}" enregistrée.')
    
    return redirect('detail_formation', pk=pk)

@login_required
def supprimer_formation(request, pk):
    employe = request.user.employe
    if employe.role != 'RH':
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')
    
    formation = get_object_or_404(Formation, pk=pk)
    if request.method == 'POST':
        formation.delete()
        messages.success(request, f'Formation "{formation.titre}" supprimée avec succès.')
        return redirect('liste_formations')
    
    context = {'formation': formation}
    return render(request, 'rh_app/formations/supprimer.html', context)

@login_required
def liste_conges(request):
    employe = request.user.employe
    
    if employe.role == 'RH':
        conges = Conge.objects.all()
    else:
        conges = Conge.objects.filter(employe=employe)
    
    context = {'conges': conges}
    return render(request, 'rh_app/conges/liste.html', context)

@login_required
def demander_conge(request):
    if request.method == 'POST':
        form = CongeForm(request.POST)
        if form.is_valid():
            conge = form.save(commit=False)
            conge.employe = request.user.employe
            conge.save()
            messages.success(request, 'Votre demande de congé a été enregistrée.')
            return redirect('liste_conges')
    else:
        form = CongeForm()
    
    return render(request, 'rh_app/conges/form.html', {'form': form, 'action': 'Demander'})

@login_required
def traiter_conge(request, pk):
    employe = request.user.employe
    if employe.role != 'RH':
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')
    
    conge = get_object_or_404(Conge, pk=pk)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action in ['APPROUVE', 'REFUSE']:
            conge.statut = action
            conge.date_reponse = timezone.now()
            conge.commentaire_rh = request.POST.get('commentaire', '')
            conge.save()
            messages.success(request, f'Congé {action.lower()}.')
            return redirect('liste_conges')
    
    context = {'conge': conge}
    return render(request, 'rh_app/conges/traiter.html', context)

@login_required
def liste_contrats(request):
    employe = request.user.employe

    if employe.role == 'RH':
        contrats = Contrat.objects.all().order_by('-date_debut')
    else:
        contrats = Contrat.objects.filter(employe=employe).order_by('-date_debut')

    contrats_actifs_count = Contrat.objects.filter(statut='ACTIF').count()
    contrats_expirant_count = Contrat.objects.filter(
        statut='ACTIF',
        date_fin__lte=timezone.now().date() + timedelta(days=30)
    ).count()
    contrats_expires_count = Contrat.objects.filter(statut='EXPIRE').count()

    context = {
        'contrats': contrats,
        'employe': employe,
        'contrats_actifs_count': contrats_actifs_count,
        'contrats_expirant_count': contrats_expirant_count,
        'contrats_expires_count': contrats_expires_count,
    }
    return render(request, 'rh_app/contrats/liste.html', context)

@login_required
def ajouter_contrat(request):
    employe = request.user.employe
    if employe.role != 'RH':
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ContratForm(request.POST, request.FILES)
        if form.is_valid():
            contrat = form.save()
            messages.success(request, f'Contrat pour {contrat.employe.get_full_name()} ajouté avec succès.')
            return redirect('liste_contrats')
    else:
        form = ContratForm()
    
    return render(request, 'rh_app/contrats/form.html', {'form': form, 'action': 'Ajouter'})

@login_required
def modifier_contrat(request, pk):
    employe = request.user.employe
    if employe.role != 'RH':
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')
    
    contrat = get_object_or_404(Contrat, pk=pk)
    
    if request.method == 'POST':
        form = ContratForm(request.POST, request.FILES, instance=contrat)
        if form.is_valid():
            form.save()
            messages.success(request, f'Contrat pour {contrat.employe.get_full_name()} modifié avec succès.')
            return redirect('liste_contrats')
    else:
        form = ContratForm(instance=contrat)
    
    return render(request, 'rh_app/contrats/form.html', {'form': form, 'action': 'Modifier'})

@login_required
def detail_contrat(request, pk):
    employe = request.user.employe
    contrat = get_object_or_404(Contrat, pk=pk)
    
    if employe.role != 'RH' and employe != contrat.employe:
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')
    
    context = {
        'contrat': contrat,
    }
    return render(request, 'rh_app/contrats/detail.html', context)

@login_required
def supprimer_contrat(request, pk):
    employe = request.user.employe
    if employe.role != 'RH':
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')
    
    contrat = get_object_or_404(Contrat, pk=pk)
    if request.method == 'POST':
        contrat.delete()
        messages.success(request, f'Contrat pour {contrat.employe.get_full_name()} supprimé avec succès.')
        return redirect('liste_contrats')
    
    context = {'contrat': contrat}
    return render(request, 'rh_app/contrats/supprimer.html', context)

@login_required
def liste_salaires(request):
    employe = getattr(request.user, 'employe', None)

    if employe and employe.role == 'RH':
        salaires = (
            Salaire.objects
            .select_related('employe', 'employe__user')
            .all()
            .order_by('-date_paiement', '-mois')
        )
    elif employe:
        salaires = (
            Salaire.objects
            .select_related('employe', 'employe__user')
            .filter(employe=employe)
            .order_by('-date_paiement', '-mois')
        )
    else:
        messages.error(request, "Aucun profil employé associé à ce compte.")
        return redirect('dashboard')

    total_salaires = salaires.count()

    context = {
        'salaires': salaires,
        'employe': employe,
        'total_salaires': total_salaires,
        'user': request.user,
    }
    return render(request, 'rh_app/salaires/liste.html', context)

@login_required
def ajouter_salaire(request):
    employe = request.user.employe
    if employe.role != 'RH':
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = SalaireForm(request.POST, request.FILES)
        if form.is_valid():
            salaire = form.save()
            messages.success(request, f'Salaire pour {salaire.employe.get_full_name()} ajouté avec succès.')
            return redirect('liste_salaires')
    else:
        form = SalaireForm()
    
    return render(request, 'rh_app/salaires/form.html', {'form': form, 'action': 'Ajouter'})

@login_required
def liste_presences(request):
    employe = request.user.employe
    
    if employe.role == 'RH':
        presences = Presence.objects.all()[:100]
    else:
        presences = Presence.objects.filter(employe=employe)[:50]
    
    context = {'presences': presences}
    return render(request, 'rh_app/presences/liste.html', context)

@login_required
def ajouter_presence(request):
    employe = request.user.employe
    if employe.role != 'RH':
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = PresenceForm(request.POST)
        if form.is_valid():
            presence = form.save()
            messages.success(request, f'Présence pour {presence.employe.get_full_name()} ajoutée.')
            return redirect('liste_presences')
    else:
        form = PresenceForm()
    
    return render(request, 'rh_app/presences/form.html', {'form': form, 'action': 'Ajouter'})

def inscription(request):
    if request.method == 'POST':
        form = EmployeSignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )

            employe = form.save(commit=False)
            employe.user = user
            employe.matricule = f"EMP{user.id:04d}"
            employe.save()

            login(request, user)
            # inform if departement was auto-created during form.save()
            if getattr(form, 'dept_created', False):
                messages.info(request, f"Le département '{employe.departement.nom}' a été créé automatiquement.")
            messages.success(request, "Votre compte a été créé et vous êtes connecté !")
            return redirect('dashboard_employe')
    else:
        form = EmployeSignupForm()
    return render(request, 'rh_app/employes/inscription.html', {'form': form})

# VUES POUR LES DÉPARTEMENTS - CORRIGÉES
@login_required
def liste_departements(request):
    employe = request.user.employe
    if employe.role != 'RH':
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')

    departements = Departement.objects.all().order_by('nom')
    context = {'departements': departements}
    return render(request, 'rh_app/departements/liste.html', context)

@login_required
def ajouter_departement(request):
    employe = request.user.employe
    if employe.role != 'RH':
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = DepartementForm(request.POST)
        if form.is_valid():
            departement = form.save()
            messages.success(request, f'Département "{departement.nom}" ajouté avec succès.')
            return redirect('liste_departements')
    else:
        form = DepartementForm()
    
    return render(request, 'rh_app/departements/form.html', {'form': form, 'action': 'Ajouter'})

@login_required
def modifier_departement(request, pk):
    employe = request.user.employe
    if employe.role != 'RH':
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')
    
    departement = get_object_or_404(Departement, pk=pk)
    
    if request.method == 'POST':
        form = DepartementForm(request.POST, instance=departement)
        if form.is_valid():
            form.save()
            messages.success(request, f'Département "{departement.nom}" modifié avec succès.')
            return redirect('liste_departements')
    else:
        form = DepartementForm(instance=departement)
    
    return render(request, 'rh_app/departements/form.html', {'form': form, 'action': 'Modifier'})

# VUE AJOUTÉE POUR CORRIGER L'ERREUR
@login_required
def detail_departement(request, pk):
    employe = request.user.employe
    if employe.role != 'RH':
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')

    departement = get_object_or_404(Departement, pk=pk)
    employes_departement = departement.employes.all()

    context = {
        'departement': departement,
        'employes_departement': employes_departement,
    }
    return render(request, 'rh_app/departements/detail.html', context)

@login_required
def supprimer_departement(request, pk):
    employe = request.user.employe
    if employe.role != 'RH':
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')

    departement = get_object_or_404(Departement, pk=pk)

    if request.method == 'POST':
        departement.delete()
        messages.success(request, f'Département "{departement.nom}" supprimé avec succès.')
        return redirect('liste_departements')

    context = {'departement': departement}
    return render(request, 'rh_app/departements/supprimer.html', context)

# VUES POUR LES DOSSIERS PERSONNELS
@login_required
def liste_dossiers_personnel(request):
    employe = request.user.employe
    
    if employe.role == 'RH':
        dossiers = DossierPersonnel.objects.all()
    else:
        dossiers = DossierPersonnel.objects.filter(employe=employe)
    
    context = {'dossiers': dossiers}
    return render(request, 'rh_app/dossiers/liste.html', context)

@login_required
def ajouter_dossier_personnel(request):
    employe = request.user.employe
    if employe.role != 'RH':
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = DossierPersonnelForm(request.POST, request.FILES)
        if form.is_valid():
            dossier = form.save()
            messages.success(request, f'Dossier "{dossier.titre}" ajouté avec succès.')
            return redirect('liste_dossiers_personnel')
    else:
        form = DossierPersonnelForm()
    
    return render(request, 'rh_app/dossiers/form.html', {'form': form, 'action': 'Ajouter'})

@login_required
def supprimer_dossier_personnel(request, pk):
    employe = request.user.employe
    if employe.role != 'RH':
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')
    
    dossier = get_object_or_404(DossierPersonnel, pk=pk)
    if request.method == 'POST':
        dossier.delete()
        messages.success(request, f'Dossier "{dossier.titre}" supprimé avec succès.')
        return redirect('liste_dossiers_personnel')
    
    context = {'dossier': dossier}
    return render(request, 'rh_app/dossiers/supprimer.html', context)

# VUES POUR LES JOURS DE TRAVAIL
@login_required
def liste_jours_travail(request):
    employe = request.user.employe
    
    if employe.role == 'RH':
        jours_travail = JourTravail.objects.all()[:100]
    else:
        jours_travail = JourTravail.objects.filter(employe=employe)[:50]
    
    context = {'jours_travail': jours_travail}
    return render(request, 'rh_app/jours_travail/liste.html', context)

@login_required
def ajouter_jour_travail(request):
    employe = request.user.employe
    if employe.role != 'RH':
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = JourTravailForm(request.POST)
        if form.is_valid():
            jour_travail = form.save()
            messages.success(request, f'Jour de travail pour {jour_travail.employe.get_full_name()} ajouté.')
            return redirect('liste_jours_travail')
    else:
        form = JourTravailForm()
    
    return render(request, 'rh_app/jours_travail/form.html', {'form': form, 'action': 'Ajouter'})

@login_required
def supprimer_jour_travail(request, pk):
    employe = request.user.employe
    if employe.role != 'RH':
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')
    
    jour_travail = get_object_or_404(JourTravail, pk=pk)
    if request.method == 'POST':
        jour_travail.delete()
        messages.success(request, f'Jour de travail supprimé avec succès.')
        return redirect('liste_jours_travail')
    
    context = {'jour_travail': jour_travail}
    return render(request, 'rh_app/jours_travail/supprimer.html', context)

# VUES DE SUPPRESSION
@login_required
def supprimer_employe(request, pk):
    employe = request.user.employe
    if employe.role != 'RH':
        messages.error(request, 'Accès non autorisé.')
        return redirect('dashboard')
    
    employe_obj = get_object_or_404(Employe, pk=pk)
    if request.method == 'POST':
        employe_obj.delete()
        messages.success(request, f'Employé {employe_obj.get_full_name()} supprimé avec succès.')
        return redirect('liste_employes')
    
    context = {'employe': employe_obj}
    return render(request, 'rh_app/employes/supprimer.html', context)