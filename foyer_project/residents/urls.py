from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profil/', views.profil, name='profil'),
    path('chambre/', views.chambre, name='chambre'),
    path('demandes/', views.demandes, name='demandes'),
    path('annonces/', views.annonces, name='annonces'),
    path('paiements/', views.paiement, name='paiements'),
    path('reglements/', views.reglements, name='reglements'),

    


]
