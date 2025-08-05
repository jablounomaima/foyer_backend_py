from django.urls import path
from . import views  # ✅ . = residents/

urlpatterns = [
     path('login/', views.login_view, name='login'),
      path('signup/', views.signup_view, name='signup'), # Add this line

      path('reservation/', views.room_reservation, name='room_reservation'),
path('reservation/status/', views.reservation_status, name='reservation_status'),
path('reservation/<int:reservation_id>/pay/', views.make_payment, name='make_payment'),
    path('dashboard/', views.dashboard, name='dashboard'),
    #path('profil/', views.index, name='profil'),
    #path('chambre/', views.chambre, name='chambre'),
    path('paiements/', views.paiements, name='paiements'),
    #path('demandes/', views.demandes, name='demandes'),
    path('annonces/', views.annonces, name='annonces'),
    path('reglements/', views.reglements, name='reglements'),
     path('reservation/', views.room_reservation, name='room_reservation'),
]