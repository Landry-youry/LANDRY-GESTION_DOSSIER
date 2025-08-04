from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as DjangoUser  
from .models import User, Employe
from .models import Dossier


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = ['poste', 'date_embauche', 'salaire', 'photo']

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = ['poste', 'date_embauche', 'salaire', 'photo']


# ➕ Formulaire combiné pour RH
class AddEmployeFullForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField()
    last_name = forms.CharField()
    poste = forms.CharField()
    date_embauche = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    salaire = forms.DecimalField()
    photo = forms.ImageField(required=False)

class DossierForm(forms.ModelForm):
    class Meta:
        model = Dossier
        fields = ['employe', 'titre', 'fichier']
