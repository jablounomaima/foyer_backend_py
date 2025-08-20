from django.urls import path
from . import views  # ✅ . = residents/
from django.conf import settings
from django.contrib.auth import views as auth_views

from django.conf.urls.static import static
urlpatterns = [
     path('', views.index, name='index'),
     path('login/', views.login_view, name='login'),
      path('signup/', views.signup_view, name='signup'), # Add this line
 path('logout/', views.logout_view, name='logout'),
      path('reservation/', views.room_reservation, name='room_reservation'),
 path('reservation/status/', views.reservation_status, name='reservation_status'),
 path('reservation/<int:reservation_id>/pay/', views.make_payment, name='make_payment'),
    path('dashboard/', views.dashboard, name='dashboard'),
path('profil/', views.profil, name='profil'),
    # residents/urls.py
path('reservation/<int:reservation_id>/payer/<str:month>/<int:year>/', 
     views.make_monthly_payment, 
     name='make_monthly_payment'),
    # residents/urls.py
path('reservation/<int:reservation_id>/pay/', views.make_payment, name='make_payment'),
    #path('profil/', views.index, name='profil'),
    #path('chambre/', views.chambre, name='chambre'),
    path('paiements/calendrier/', views.payment_calendar, name='payment_calendar'),
 path('paiements/', views.paiements, name='paiements'),  # ✅ Ajouté    
path('paiements/', views.payment_history, name='payment_history'),
path('paiements/<int:reservation_id>/<str:month>/<int:year>/', views.make_monthly_payment, name='make_monthly_payment'),
    #path('demandes/', views.demandes, name='demandes'),
    path('annonces/', views.annonces, name='annonces'),
    path('reglements/', views.reglements, name='reglements'),
    #ajouter une button pour telecharger les images de reglement 
    path('reglements/telecharger_tout/', views.download_all_reglements, name='download_all_reglements'),
    path('reglements/telecharger_tout_jpg/', views.download_all_reglements_as_jpg, name='download_all_reglements_as_jpg'),

    # residents/urls.py
path('tarifs/', views.room_pricing, name='room_pricing'),
     path('reservation/', views.room_reservation, name='room_reservation'),






    # Demander l'email pour la réinitialisation du mot de passe
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='residents/password_reset_form.html'), name='password_reset'),

    # Page confirmant que le mail a été envoyé
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='residents/password_reset_done.html'), name='password_reset_done'),

    # Lien reçu dans le mail, formulaire pour entrer un nouveau mot de passe
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='residents/password_reset_confirm.html'), name='password_reset_confirm'),

    # Confirmation que le mot de passe a bien été changé
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='residents/password_reset_complete.html'), name='password_reset_complete'),





]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)