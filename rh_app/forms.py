from django import forms
from .models import Employe, Formation, InscriptionFormation, Conge, Contrat, Salaire, Presence, Departement, DossierPersonnel, JourTravail
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label='Nom d\'utilisateur',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom d\'utilisateur'})
    )
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'})
    )

class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        exclude = ['user']
        widgets = {
            'matricule': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date_naissance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_embauche': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'poste': forms.TextInput(attrs={'class': 'form-control'}),
            'departement': forms.Select(attrs={'class': 'form-control'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

class FormationForm(forms.ModelForm):
    class Meta:
        model = Formation
        fields = '__all__'
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'lieu': forms.TextInput(attrs={'class': 'form-control'}),
            'formateur': forms.TextInput(attrs={'class': 'form-control'}),
            'capacite': forms.NumberInput(attrs={'class': 'form-control'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
        }

class InscriptionFormationForm(forms.ModelForm):
    class Meta:
        model = InscriptionFormation
        fields = ['formation', 'note']
        widgets = {
            'formation': forms.Select(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CongeForm(forms.ModelForm):
    # Optionnel: permet de demander un congé en nombre de mois
    mois = forms.IntegerField(
        required=False,
        min_value=1,
        label='Nombre de mois (optionnel)',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Conge
        fields = ['type_conge', 'date_debut', 'date_fin', 'nombre_jours', 'motif', 'mois']
        widgets = {
            'type_conge': forms.Select(attrs={'class': 'form-control'}),
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'nombre_jours': forms.NumberInput(attrs={'class': 'form-control'}),
            'motif': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def clean(self):
        cleaned = super().clean()
        date_debut = cleaned.get('date_debut')
        date_fin = cleaned.get('date_fin')
        mois = cleaned.get('mois')

        # Si l'utilisateur fournit un nombre de mois, on calcule automatiquement la date de fin
        if date_debut and mois:
            # Calcul d'ajout de mois sans dépendances externes
            year = date_debut.year
            month = date_debut.month + mois
            day = date_debut.day

            # normaliser l'année/mois
            year += (month - 1) // 12
            month = ((month - 1) % 12) + 1

            # trouver le dernier jour du mois cible si le jour d'origine n'existe pas
            import calendar
            last_day = calendar.monthrange(year, month)[1]
            day = min(day, last_day)

            from datetime import date, timedelta
            computed_end = date(year, month, day) - timedelta(days=1)
            # si on veut inclure exactement N mois complets, on part du 1er jour suivant
            # Ajuster pour couvrir au moins un jour
            if computed_end < date_debut:
                computed_end = date_debut

            cleaned['date_fin'] = computed_end
            date_fin = computed_end

        # Valider cohérence dates
        if date_debut and date_fin and date_fin < date_debut:
            from django.core.exceptions import ValidationError
            raise ValidationError('La date de fin doit être postérieure ou égale à la date de début.')

        # Calculer automatiquement le nombre de jours si dates présentes
        if date_debut and date_fin:
            from datetime import timedelta
            cleaned['nombre_jours'] = (date_fin - date_debut).days + 1

        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        # S'assurer que nombre_jours est cohérent avec les dates
        if instance.date_debut and instance.date_fin:
            instance.nombre_jours = (instance.date_fin - instance.date_debut).days + 1
        if commit:
            instance.save()
        return instance

class ContratForm(forms.ModelForm):
    class Meta:
        model = Contrat
        fields = '__all__'
        widgets = {
            'employe': forms.Select(attrs={'class': 'form-control'}),
            'type_contrat': forms.Select(attrs={'class': 'form-control'}),
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'salaire_base': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'poste': forms.TextInput(attrs={'class': 'form-control'}),
            'departement': forms.TextInput(attrs={'class': 'form-control'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
            'document': forms.FileInput(attrs={'class': 'form-control'}),
        }

class SalaireForm(forms.ModelForm):
    class Meta:
        model = Salaire
        exclude = ['salaire_net']
        widgets = {
            'employe': forms.Select(attrs={'class': 'form-control'}),
            'mois': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 12}),
            'annee': forms.NumberInput(attrs={'class': 'form-control'}),
            'salaire_base': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            # primes and deductions removed from the form per request
            'date_paiement': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'bulletin': forms.FileInput(attrs={'class': 'form-control'}),
        }

class PresenceForm(forms.ModelForm):
    class Meta:
        model = Presence
        exclude = ['date_creation']
        widgets = {
            'employe': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'heure_arrivee': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'heure_depart': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }




# POur inscription des employés
class EmployeSignupForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        label='Nom d’utilisateur',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom d’utilisateur'})
    )
    password1 = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'})
    )
    password2 = forms.CharField(
        label='Confirmer le mot de passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmer le mot de passe'})
    )

    # allow users to type a department name at signup; we'll convert it to a Departement instance on save
    departement = forms.CharField(
        required=False,
        label='Département',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Informatique'})
    )

    class Meta:
        model = Employe
        # exclude the model FK 'departement' so the form's text field doesn't get assigned directly
        exclude = ['user', 'matricule', 'role', 'statut', 'photo', 'departement']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date_naissance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'poste': forms.TextInput(attrs={'class': 'form-control'}),
            'date_embauche': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        if User.objects.filter(username=cleaned_data.get("username")).exists():
            raise forms.ValidationError("Ce nom d’utilisateur est déjà pris.")
        if Employe.objects.filter(email=cleaned_data.get("email")).exists():
            raise ValidationError("Cet email est déjà utilisé.")
        return cleaned_data

    def save(self, commit=True):
        # convert departement text to Departement instance (create if missing)
        instance = super().save(commit=False)
        departement_name = self.cleaned_data.get('departement')
        # default: no new dept created
        self.dept_created = False
        if departement_name:
            # normalize name
            name = departement_name.strip()
            # Try to get or create in a transaction to avoid race conditions
            try:
                with transaction.atomic():
                    dept_obj, created = Departement.objects.get_or_create(nom__iexact=name, defaults={'nom': name})
                    if created:
                        self.dept_created = True
            except IntegrityError:
                # possible parallel creation; fallback to retrieving
                dept_obj = Departement.objects.filter(nom__iexact=name).first()
                if not dept_obj:
                    raise
            instance.departement = dept_obj
        if commit:
            instance.save()
        return instance

class DepartementForm(forms.ModelForm):
    class Meta:
        model = Departement
        fields = '__all__'
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'responsable': forms.Select(attrs={'class': 'form-control'}),
            'budget_annuel': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class DossierPersonnelForm(forms.ModelForm):
    class Meta:
        model = DossierPersonnel
        fields = '__all__'
        widgets = {
            'employe': forms.Select(attrs={'class': 'form-control'}),
            'type_document': forms.Select(attrs={'class': 'form-control'}),
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'document': forms.FileInput(attrs={'class': 'form-control'}),
            'date_expiration': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'confidentiel': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class JourTravailForm(forms.ModelForm):
    class Meta:
        model = JourTravail
        fields = '__all__'
        widgets = {
            'employe': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'heures_travaillees': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'min': '0', 'max': '24'}),
            'heures_supplementaires': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'min': '0'}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'valide': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
