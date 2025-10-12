from django import forms
from .models import Employe, Departement, Formation, Conge, Contrat, Salaire, JourDeTravail


# =========================================================
# FORMULAIRES DES EMPLOYÉS ET DÉPARTEMENTS
# =========================================================

class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = [
            'user', 'matricule', 'nom', 'prenom', 'sexe',
            'date_naissance', 'email', 'telephone', 'adresse',
            'date_embauche', 'departement'
        ]
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
            'date_embauche': forms.DateInput(attrs={'type': 'date'}),
            'sexe': forms.Select(choices=[('M', 'Masculin'), ('F', 'Féminin')]),
        }


class DepartementForm(forms.ModelForm):
    class Meta:
        model = Departement
        fields = ['nom', 'date_fin']
        widgets = {
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }


# =========================================================
# FORMULAIRES DES FORMATIONS, CONTRATS ET SALAIRES
# =========================================================

class FormationForm(forms.ModelForm):
    class Meta:
        model = Formation
        fields = ['intitule_formation', 'organisme', 'date_formation', 'cout', 'personnel_suivi']
        widgets = {
            'date_formation': forms.DateInput(attrs={'type': 'date'}),
            'cout': forms.NumberInput(attrs={'step': '0.01'}),
            'personnel_suivi': forms.SelectMultiple(attrs={'size': 6}),
        }


class ContratForm(forms.ModelForm):
    class Meta:
        model = Contrat
        fields = ['type_contrat', 'date_debut', 'date_fin', 'employe']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
            'type_contrat': forms.Select(),
        }


class SalaireForm(forms.ModelForm):
    class Meta:
        model = Salaire
        fields = ['employe', 'montant_base', 'montant_net', 'date_effective', 'periode']
        widgets = {
            'date_effective': forms.DateInput(attrs={'type': 'date'}),
            'montant_base': forms.NumberInput(attrs={'step': '0.01'}),
            'montant_net': forms.NumberInput(attrs={'step': '0.01'}),
            'periode': forms.TextInput(),
        }


# =========================================================
# FORMULAIRES DES CONGÉS ET JOURS DE TRAVAIL
# =========================================================

class CongeForm(forms.ModelForm):
    class Meta:
        model = Conge
        fields = ['date_debut', 'date_fin', 'motif']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
            'motif': forms.Textarea(attrs={'rows': 3}),
        }


class JourDeTravailForm(forms.ModelForm):
    class Meta:
        model = JourDeTravail
        fields = ['jour', 'heure_debut', 'heure_fin', 'statut', 'employes']
        widgets = {
            'heure_debut': forms.TimeInput(attrs={'type': 'time'}),
            'heure_fin': forms.TimeInput(attrs={'type': 'time'}),
            'employes': forms.SelectMultiple(attrs={'size': 6}),
        }
