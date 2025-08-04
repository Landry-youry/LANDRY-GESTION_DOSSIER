from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from django.contrib import messages
from .models import User
from .models import Employe
from django.contrib.auth.decorators import login_required
from .forms import AddEmployeFullForm
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from .models import Dossier
from .forms import DossierForm
from django.views.decorators.http import require_POST



def home(request):
    return render(request, 'personnel/home.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connexion auto après inscription
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'personnel/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Nom d’utilisateur ou mot de passe invalide')
    return render(request, 'personnel/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def employe_list(request):
    if not request.user.is_rh:
        return redirect('home')  # accès réservé RH

    employes = Employe.objects.all()
    return render(request, 'personnel/employe_list.html', {'employes': employes})

@login_required
def add_employe(request):
    if not request.user.is_rh:
        return redirect('home')

    if request.method == 'POST':
        form = AddEmployeFullForm(request.POST, request.FILES)
        if form.is_valid():
            # Créer l'utilisateur
            user = User.objects.create(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=make_password(form.cleaned_data['password']),
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )

            # Créer l'employé lié
            Employe.objects.create(
                user=user,
                poste=form.cleaned_data['poste'],
                date_embauche=form.cleaned_data['date_embauche'],
                salaire=form.cleaned_data['salaire'],
                photo=form.cleaned_data.get('photo')
            )
            return redirect('employe_list')
    else:
        form = AddEmployeFullForm()

    return render(request, 'personnel/add_employe.html', {'form': form})


@login_required
def edit_employe(request, pk):
    if not request.user.is_rh:
        return redirect('home')
    employe = get_object_or_404(Employe, pk=pk)
    if request.method == 'POST':
        form = AddEmployeFullForm(request.POST, request.FILES)
        if form.is_valid():
            user = employe.user
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])
            user.save()

            employe.poste = form.cleaned_data['poste']
            employe.date_embauche = form.cleaned_data['date_embauche']
            employe.salaire = form.cleaned_data['salaire']
            if form.cleaned_data.get('photo'):
                employe.photo = form.cleaned_data['photo']
            employe.save()

            return redirect('employe_list')
    else:
        form = AddEmployeFullForm(initial={
            'username': employe.user.username,
            'email': employe.user.email,
            'first_name': employe.user.first_name,
            'last_name': employe.user.last_name,
            'poste': employe.poste,
            'date_embauche': employe.date_embauche,
            'salaire': employe.salaire,
        })
    return render(request, 'personnel/edit_employe.html', {'form': form, 'employe': employe})


@login_required
def delete_employe(request, pk):
    if not request.user.is_rh:
        return redirect('home')
    employe = get_object_or_404(Employe, pk=pk)
    if request.method == 'POST':
        user = employe.user
        employe.delete()
        user.delete()
        return redirect('employe_list')
    return render(request, 'personnel/delete_employe.html', {'employe': employe})


@login_required
def dossier_list(request):
    if not request.user.is_rh:
        return redirect('home')
    dossiers = Dossier.objects.all().order_by('-date_ajout')
    return render(request, 'personnel/dossier_list.html', {'dossiers': dossiers})

@login_required
def add_dossier(request):
    if not request.user.is_rh:
        return redirect('home')
    if request.method == 'POST':
        form = DossierForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dossier_list')
    else:
        form = DossierForm()
    return render(request, 'personnel/add_dossier.html', {'form': form})

@login_required
def delete_dossier(request, pk):
    if not request.user.is_rh:
        return redirect('home')
    dossier = get_object_or_404(Dossier, pk=pk)
    if request.method == 'POST':
        dossier.delete()
        return redirect('dossier_list')
    return render(request, 'personnel/delete_dossier.html', {'dossier': dossier})


@login_required
def gestion_roles(request):
    if not request.user.is_rh:
        return redirect('home')
    
    users = User.objects.all().exclude(id=request.user.id)  # ne pas afficher soi-même
    return render(request, 'personnel/gestion_roles.html', {'users': users})


@require_POST
@login_required
def toggle_rh(request, user_id):
    if not request.user.is_rh:
        return redirect('home')
    
    user = get_object_or_404(User, pk=user_id)
    user.is_rh = not user.is_rh
    user.save()
    return redirect('gestion_roles')





