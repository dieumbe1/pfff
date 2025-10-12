from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import (
    Departement, Employe, Formation, Conge,
    Contrat, Salaire, JourDeTravail
)
from .forms import (
    EmployeForm, DepartementForm, FormationForm,
    CongeForm, ContratForm, SalaireForm, JourDeTravailForm
)

# =================== ACCUEIL ET DASHBOARDS ===================

@login_required
def accueil(request):
    return render(request, 'gestion_rh/accueil.html')

@login_required
def responsable_rh(request):
    return render(request, 'gestion_rh/dashboard_rh.html')

@login_required
def employe_dashboard(request):
    return render(request, 'gestion_rh/dashboard_employe.html')

# =================== DÉPARTEMENTS ===================

@login_required
def liste_departements(request):
    departements = Departement.objects.all()
    return render(request, 'gestion_rh/liste_departements.html', {'departements': departements})

@login_required
def ajouter_departement(request):
    if request.method == 'POST':
        form = DepartementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_departements')
    else:
        form = DepartementForm()
    return render(request, 'gestion_rh/ajouter_departement.html', {'form': form})

@login_required
def modifier_departement(request, pk):
    departement = get_object_or_404(Departement, pk=pk)
    if request.method == 'POST':
        form = DepartementForm(request.POST, instance=departement)
        if form.is_valid():
            form.save()
            return redirect('liste_departements')
    else:
        form = DepartementForm(instance=departement)
    return render(request, 'gestion_rh/modifier_departement.html', {'form': form})

@login_required
def supprimer_departement(request, pk):
    departement = get_object_or_404(Departement, pk=pk)
    if request.method == 'POST':
        departement.delete()
        return redirect('liste_departements')
    return render(request, 'gestion_rh/supprimer_departement.html', {'departement': departement})

# =================== EMPLOYÉS ===================

@login_required
def liste_employes(request):
    employes = Employe.objects.all()
    return render(request, 'gestion_rh/liste_employes.html', {'employes': employes})

@login_required
def ajouter_employe(request):
    if request.method == 'POST':
        form = EmployeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_employes')
    else:
        form = EmployeForm()
    return render(request, 'gestion_rh/ajouter_employe.html', {'form': form})

@login_required
def modifier_employe(request, pk):
    employe = get_object_or_404(Employe, pk=pk)
    if request.method == 'POST':
        form = EmployeForm(request.POST, instance=employe)
        if form.is_valid():
            form.save()
            return redirect('liste_employes')
    else:
        form = EmployeForm(instance=employe)
    return render(request, 'gestion_rh/modifier_employe.html', {'form': form})

@login_required
def supprimer_employe(request, pk):
    employe = get_object_or_404(Employe, pk=pk)
    if request.method == 'POST':
        employe.delete()
        return redirect('liste_employes')
    return render(request, 'gestion_rh/supprimer_employe.html', {'employe': employe})

# =================== FORMATIONS ===================

@login_required
def liste_formations(request):
    formations = Formation.objects.all()
    return render(request, 'gestion_rh/liste_formations.html', {'formations': formations})

@login_required
def ajouter_formation(request):
    if request.method == 'POST':
        form = FormationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_formations')
    else:
        form = FormationForm()
    return render(request, 'gestion_rh/ajouter_formation.html', {'form': form})

@login_required
def modifier_formation(request, pk):
    formation = get_object_or_404(Formation, pk=pk)
    if request.method == 'POST':
        form = FormationForm(request.POST, instance=formation)
        if form.is_valid():
            form.save()
            return redirect('liste_formations')
    else:
        form = FormationForm(instance=formation)
    return render(request, 'gestion_rh/modifier_formation.html', {'form': form})

@login_required
def supprimer_formation(request, pk):
    formation = get_object_or_404(Formation, pk=pk)
    if request.method == 'POST':
        formation.delete()
        return redirect('liste_formations')
    return render(request, 'gestion_rh/supprimer_formation.html', {'formation': formation})

@login_required
def mes_formations(request):
    employe = get_object_or_404(Employe, user=request.user)
    formations = employe.formations_suivies.all()
    return render(request, 'gestion_rh/mes_formations.html', {'formations': formations})

# =================== CONGÉS ===================

@login_required
def liste_conges(request):
    conges = Conge.objects.all()
    return render(request, 'gestion_rh/liste_conges.html', {'conges': conges})

@login_required
def ajouter_conge(request):
    if request.method == 'POST':
        form = CongeForm(request.POST)
        if form.is_valid():
            conge = form.save(commit=False)
            conge.employe = get_object_or_404(Employe, user=request.user)
            conge.save()
            return redirect('liste_conges')
    else:
        form = CongeForm()
    return render(request, 'gestion_rh/ajouter_conge.html', {'form': form})

# =================== CONTRATS ===================

@login_required
def liste_contrats(request):
    contrats = Contrat.objects.all()
    return render(request, 'gestion_rh/liste_contrats.html', {'contrats': contrats})

@login_required
def ajouter_contrat(request):
    if request.method == 'POST':
        form = ContratForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_contrats')
    else:
        form = ContratForm()
    return render(request, 'gestion_rh/ajouter_contrat.html', {'form': form})

# =================== SALAIRES ===================

@login_required
def liste_salaires(request):
    salaires = Salaire.objects.all()
    return render(request, 'gestion_rh/liste_salaires.html', {'salaires': salaires})

@login_required
def ajouter_salaire(request):
    if request.method == 'POST':
        form = SalaireForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_salaires')
    else:
        form = SalaireForm()
    return render(request, 'gestion_rh/ajouter_salaire.html', {'form': form})

# =================== JOURS DE TRAVAIL ===================

@login_required
def liste_jours_travail(request):
    jours = JourDeTravail.objects.all()
    return render(request, 'gestion_rh/liste_jours_travail.html', {'jours': jours})

@login_required
def ajouter_jour_travail(request):
    if request.method == 'POST':
        form = JourDeTravailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_jours_travail')
    else:
        form = JourDeTravailForm()
    return render(request, 'gestion_rh/ajouter_jour_travail.html', {'form': form})

@login_required
def modifier_jour_travail(request, pk):
    jour = get_object_or_404(JourDeTravail, pk=pk)
    if request.method == 'POST':
        form = JourDeTravailForm(request.POST, instance=jour)
        if form.is_valid():
            form.save()
            return redirect('liste_jours_travail')
    else:
        form = JourDeTravailForm(instance=jour)
    return render(request, 'gestion_rh/modifier_jour_travail.html', {'form': form, 'jour': jour})

@login_required
def supprimer_jour_travail(request, pk):
    jour = get_object_or_404(JourDeTravail, pk=pk)
    if request.method == 'POST':
        jour.delete()
        return redirect('liste_jours_travail')
    return render(request, 'gestion_rh/supprimer_jour_travail.html', {'jour': jour})
