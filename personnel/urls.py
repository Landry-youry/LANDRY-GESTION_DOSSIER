from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('employes/', views.employe_list, name='employe_list'),
    path('employes/ajouter/', views.add_employe, name='add_employe'),
    path('employes/modifier/<int:pk>/', views.edit_employe, name='edit_employe'),
    path('employes/supprimer/<int:pk>/', views.delete_employe, name='delete_employe'),
    path('dossiers/', views.dossier_list, name='dossier_list'),
    path('dossiers/ajouter/', views.add_dossier, name='add_dossier'),
    path('dossiers/supprimer/<int:pk>/', views.delete_dossier, name='delete_dossier'),
    path('roles/', views.gestion_roles, name='gestion_roles'),
    path('roles/toggle/<int:user_id>/', views.toggle_rh, name='toggle_rh'),

]
