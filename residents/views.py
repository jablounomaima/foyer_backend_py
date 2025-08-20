# residents/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render
from .models import RoomPricing
from .models import RoomPricing  # Importez le modèle
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PaymentForm, ResidentCreationForm
from .models import MonthlyPayment, RoomPricing

# residents/views.py
from .models import MonthlyPayment, RoomPricing
from .models import Reservation
from .forms import ProfileForm, ResidentSignupForm, ReservationForm
# residents/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Reservation, Payment
# --- Vues d'authentification ---

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'residents/login.html', {'form': form})
from django.contrib.auth import login
def signup_view(request):
    if request.method == 'POST':
        form = ResidentCreationForm(request.POST)
        if form.is_valid():  # ⚠️ C’est ici que ça plante si mal configuré
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # ou une autre page
        else:
            print("Erreurs du formulaire :", form.errors)  # 🔍 Pour déboguer
    else:
        form = ResidentCreationForm()

    return render(request, 'residents/signup.html', {'form': form})
# --- Vues principales ---

@login_required
def dashboard(request):
    return render(request, 'residents/dashboard.html')

@login_required
def profil(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès.")
            return redirect('profil')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'residents/profil.html', {'form': form})
# --- Vues de réservation ---

# residents/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Reservation, RoomPricing  # Importez RoomPricing

@login_required
def room_reservation(request):
    # Vérifier si le résident a déjà une réservation active
    existing_reservation = Reservation.objects.filter(
        resident=request.user
    ).exclude(status='cancelled').first()

    if existing_reservation:
        messages.info(request, f"Vous avez déjà une réservation {existing_reservation.get_status_display()}.")
        return redirect('reservation_status')

    # Récupérer tous les tarifs
    pricing = RoomPricing.objects.all()

    if request.method == 'POST':
        form = ReservationForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre demande de réservation a été envoyée. En attente d'approbation.")
            return redirect('reservation_status')
    else:
        form = ReservationForm()

    return render(request, 'residents/room_reservation.html', {
        'form': form,
        'pricing': pricing  # Envoyer les tarifs au template
    })
@login_required
def reservation_status(request):
    reservation = Reservation.objects.filter(resident=request.user).order_by('-requested_at').first()
    return render(request, 'residents/reservation_status.html', {'reservation': reservation})

# residents/views.py

# residents/views.py

# residents/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Reservation, Payment

# residents/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Reservation, Payment

# residents/views.py

# residents/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Reservation, Payment


# ✅ Version corrigée de make_payment
@login_required
def make_payment(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, resident=request.user)

    if reservation.status != 'approved':
        messages.error(request, "Le paiement n'est pas disponible pour cette réservation.")
        return redirect('reservation_status')

    if timezone.now() > reservation.payment_deadline:
        reservation.status = 'cancelled'
        reservation.save()
        messages.error(request, "Délai de paiement expiré. Réservation annulée.")
        return redirect('reservation_status')

    if hasattr(reservation, 'payment'):
        messages.warning(request, "Un paiement a déjà été soumis pour cette réservation. En attente de vérification.")
        return redirect('reservation_status')

    if request.method == 'POST':
        method = request.POST.get('method')
        proof = request.FILES.get('proof')
        notes = request.POST.get('notes')

        if method and proof:
            # ✅ Correction : Création manuelle → il faut TOUT assigner
            payment = Payment()
            payment.reservation = reservation
            payment.resident = reservation.resident  # ✅ Obligatoire
            payment.amount = reservation.get_price() + reservation.get_deposit()
            payment.method = method
            payment.proof = proof
            payment.notes = notes
            payment.status = 'pending'
            payment.save()  # ✅ Maintenant, pas d'erreur

            messages.success(request, "Votre paiement a été envoyé. En attente de vérification.")
            return redirect('reservation_status')
        else:
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")

    return render(request, 'residents/make_payment.html', {'reservation': reservation})# residents/views.py
@login_required
def paiements(request):
    # Utilisez 'created_at' au lieu de 'paid_at'
    payments = Payment.objects.filter(reservation__resident=request.user).order_by('-created_at')
    
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.reservation = request.user.reservation_set.filter(status='approved').first()
            payment.amount = 350  # ou calculer selon RoomPricing
            payment.save()
            messages.success(request, "Votre paiement a été envoyé. En attente de vérification.")
            return redirect('paiements')
    else:
        form = PaymentForm()

    return render(request, 'residents/paiements.html', {
        'form': form,
        'payments': payments
    })
@login_required
def annonces(request):
    return render(request, 'residents/annonces.html')



from .models import ReglementImage

@login_required
def reglements(request):
    print("reglements view appelée")  # Pour debug console serveur
    reglements = ReglementImage.objects.filter(mis_en_ligne=True).order_by('ordre')
    return render(request, 'residents/reglements.html', {'reglements': reglements})




# residents/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Reservation, Payment
from .forms import PaymentForm

# residents/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Reservation
from .forms import PaymentForm


@login_required
def make_payment(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, resident=request.user)

    # Vérifier le statut
    if reservation.status != 'approved':
        messages.error(request, "Le paiement n'est pas disponible pour cette réservation.")
        return redirect('reservation_status')

    # Vérifier le délai
    if timezone.now() > reservation.payment_deadline:
        reservation.status = 'cancelled'
        reservation.save()
        messages.error(request, "Délai de paiement expiré. Réservation annulée.")
        return redirect('reservation_status')

    # Vérifier si un paiement existe déjà
    if hasattr(reservation, 'payment'):
        messages.warning(request, "Un paiement a déjà été soumis pour cette réservation.")
        return redirect('reservation_status')

    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.reservation = reservation
            payment.resident = reservation.resident  # ✅ CORRECTION ICI
            payment.amount = reservation.get_price() + reservation.get_deposit()
            payment.save()  # ✅ Maintenant, pas d'erreur
            messages.success(request, "Votre paiement a été envoyé. En attente de vérification.")
            return redirect('reservation_status')
        else:
            messages.error(request, "Veuillez remplir tous les champs.")
    else:
        form = PaymentForm()

    return render(request, 'residents/make_payment.html', {
        'reservation': reservation,
        'form': form
    })


def room_pricing(request):
    pricing = RoomPricing.objects.all()
  
    return render(request, 'residents/room_pricing.html', {'pricing': pricing})


@login_required
def dashboard(request):
    # Récupérer tous les tarifs
    pricing = RoomPricing.objects.all()
    return render(request, 'residents/dashboard.html', {'pricing': pricing})




# residents/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import MonthlyPayment, RoomPricing

@login_required
def payment_history(request):
    # Trouver la réservation active
    reservation = request.user.reservation_set.filter(status='paid').first()
    if not reservation:
        messages.error(request, "Aucune réservation active.")
        return redirect('dashboard')

    # Générer les 12 derniers mois
    from datetime import date
    today = date.today()
    months = []
    for i in range(12):
        month_date = today.replace(year=today.year - (i // 12), month=((today.month - i - 1) % 12) + 1)
        month_name = month_date.strftime("%B").lower()
        year = month_date.year

        # Trouver le tarif
        pricing = RoomPricing.objects.get(room_type=reservation.room_type)
        amount = pricing.monthly_rent

        # Vérifier si le paiement existe
        try:
            payment = MonthlyPayment.objects.get(reservation=reservation, month=month_name, year=year)
            status = payment.status
            proof_url = payment.proof.url if payment.proof else None
        except MonthlyPayment.DoesNotExist:
            payment = None
            status = 'overdue' if month_date < today else 'pending'
            proof_url = None

        months.append({
            'month': month_date.strftime("%B %Y"),
            'amount': amount,
            'status': status,
            'payment': payment,
            'proof_url': proof_url,
            'can_pay': status in ['pending', 'overdue']
        })

    return render(request, 'residents/payment_history.html', {'months': months, 'reservation': reservation})

# residents/views.py



# residents/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Reservation, MonthlyPayment, RoomPricing
from .forms import PaymentForm

@login_required
def make_monthly_payment(request, reservation_id, month, year):
    reservation = get_object_or_404(Reservation, id=reservation_id, resident=request.user)

    # Convertir le mois (slug) en format valide si nécessaire
    month_names = {
        'janvier': 'janvier', 'fevrier': 'février', 'mars': 'mars',
        'avril': 'avril', 'mai': 'mai', 'juin': 'juin',
        'juillet': 'juillet', 'aout': 'août', 'septembre': 'septembre',
        'octobre': 'octobre', 'novembre': 'novembre', 'decembre': 'décembre'
    }
    month_key = month_names.get(month, month)

    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            pricing = RoomPricing.objects.get(room_type=reservation.room_type)
            payment = form.save(commit=False)
            payment.reservation = reservation
            payment.payment_type = 'monthly'
            payment.amount = pricing.monthly_rent
            payment.status = 'pending'
            payment.save()

            # Créer l'entrée dans MonthlyPayment
            MonthlyPayment.objects.update_or_create(
                reservation=reservation,
                month=month_key,
                year=int(year),
                defaults={'amount': payment.amount, 'status': 'pending'}
            )

            messages.success(request, f"Paiement de {month} {year} envoyé. En attente de vérification.")
            return redirect('payment_calendar')
        else:
            messages.error(request, "Veuillez remplir tous les champs.")
    else:
        form = PaymentForm()

    return render(request, 'residents/make_monthly_payment.html', {
        'form': form,
        'reservation': reservation,
        'month': month,
        'year': year
    })
# residents/views.py
# residents/views.py
# residents/views.py
@login_required
def payment_calendar(request):
    reservation = Reservation.objects.filter(resident=request.user, status='paid').first()
    if not reservation:
        return render(request, 'residents/payment_calendar.html', {'error': "Aucune réservation active."})

    today = timezone.now().date()
    months = []

    for i in range(12):
        month_date = today.replace(year=today.year - (i // 12), month=((today.month - i - 1) % 12) + 1)
        month_name = month_date.strftime("%B").lower()
        year = month_date.year

        month_map = {
            'janvier': 'janvier', 'février': 'fevrier', 'mars': 'mars',
            'avril': 'avril', 'mai': 'mai', 'juin': 'juin',
            'juillet': 'juillet', 'août': 'aout', 'septembre': 'septembre',
            'octobre': 'octobre', 'novembre': 'novembre', 'décembre': 'decembre'
        }
        month_key = month_map.get(month_name, month_name)

        try:
            monthly_payment = MonthlyPayment.objects.get(reservation=reservation, month=month_key, year=year)
            status = monthly_payment.status
        except MonthlyPayment.DoesNotExist:
            status = 'overdue' if month_date < today else 'pending'

        months.append({
            'date': month_date,
            'month': month_key,
            'year': year,
            'status': status,
            'can_pay': status in ['pending', 'overdue'],
            'payment': monthly_payment if status != 'pending' else None
        })
         # ... génération des mois ...
    return render(request, 'residents/payment_calendar.html', {
        'months': months,
        'reservation': reservation  # ✅ Passé ici
    })

    
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Reservation, Payment, MonthlyPayment, RoomPricing

# residents/views.py
@login_required
def make_initial_payment(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, resident=request.user)

    if reservation.status != 'approved':
        messages.error(request, "Pas de réservation approuvée.")
        return redirect('reservation_status')

    if Payment.objects.filter(reservation=reservation, payment_type='initial').exists():
        messages.info(request, "Le paiement initial a déjà été envoyé.")
        return redirect('reservation_status')

    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            pricing = RoomPricing.objects.get(room_type=reservation.room_type)
            total_amount = pricing.monthly_rent + pricing.deposit

            payment = form.save(commit=False)
            payment.reservation = reservation
            payment.payment_type = 'initial'
            payment.amount = total_amount
            payment.save()

            # 🔴 Créer l'entrée pour le mois en cours
            now = timezone.now()
            month_name = now.strftime("%B").lower()
            year = now.year

            month_map = {
                'janvier': 'janvier', 'février': 'fevrier', 'mars': 'mars',
                'avril': 'avril', 'mai': 'mai', 'juin': 'juin',
                'juillet': 'juillet', 'août': 'aout', 'septembre': 'septembre',
                'octobre': 'octobre', 'novembre': 'novembre', 'décembre': 'decembre'
            }
            month_key = month_map.get(month_name, month_name)

            MonthlyPayment.objects.get_or_create(
                reservation=reservation,
                month=month_key,
                year=year,
                defaults={
                    'amount': pricing.monthly_rent,
                    'status': 'pending'
                }
            )

            reservation.status = 'paid'
            reservation.save()

            messages.success(request, "Paiement initial envoyé. Bienvenue !")
            return redirect('payment_calendar')
        else:
            messages.error(request, "Veuillez remplir tous les champs.")
    else:
        form = PaymentForm()

    return render(request, 'residents/make_initial_payment.html', {'form': form, 'reservation': reservation})


from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('login')  # Redirige vers la page de connexion




# residents/views.py
from django.shortcuts import render
from .models import RoomPricing

from django.shortcuts import render
from .models import RoomPricing, ReglementImage

def index(request):
    # Récupérer tous les tarifs
    room_pricings = RoomPricing.objects.all()

    # Récupérer 3 images du règlement pour un aperçu
    reglements_preview = ReglementImage.objects.filter(mis_en_ligne=True).order_by('ordre')[:3]

    return render(request, 'residents/index.html', {
        'room_pricings': room_pricings,
        'reglements_preview': reglements_preview
    })






# residents/views.py
from django.shortcuts import render
from .models import ReglementImage

# afficher l'image dans reglement.html 
from django.shortcuts import render
from .models import ReglementImage  # ✅ Import obligatoire
from django.shortcuts import render
from .models import ReglementImage

def reglements_view(request):
    print("reglements_view appelée")
    reglements = ReglementImage.objects.filter(mis_en_ligne=True).order_by('ordre')
    print(f"Images trouvées: {reglements.count()}")
    for r in reglements:
        print(f"Image: {r.titre} - URL: {r.image.url}")
    return render(request, 'residents/reglements.html', {'reglements': reglements})

# residents/views.py
from .models import ReglementImage
from django.shortcuts import render

def reglement_resident(request):
    reglements = ReglementImage.objects.filter(mis_en_ligne=True).order_by('ordre')
    return render(request, 'residents/reglement.html', {'reglements': reglements})


import os
import zipfile
from io import BytesIO
from django.http import HttpResponse
from django.conf import settings
from .models import ReglementImage

@login_required
def download_all_reglements(request):
    # Crée un buffer en mémoire pour le fichier ZIP
    zip_buffer = BytesIO()

    # Créer un zip dans ce buffer
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        images = ReglementImage.objects.filter(mis_en_ligne=True)
        for image in images:
            # Chemin complet du fichier sur disque
            image_path = os.path.join(settings.MEDIA_ROOT, image.image.name)

            # Nom du fichier dans le zip (juste le nom, pas tout le chemin)
            filename = os.path.basename(image_path)

            # Ajouter le fichier dans le zip
            zip_file.write(image_path, arcname=filename)

    # Préparer la réponse HTTP pour le téléchargement
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=reglements.zip'

    return response



import os
import zipfile
from io import BytesIO
from django.http import HttpResponse
from django.conf import settings
from .models import ReglementImage

@login_required
def download_all_reglements_as_jpg(request):
    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        images = ReglementImage.objects.filter(mis_en_ligne=True)
        for image in images:
            image_path = os.path.join(settings.MEDIA_ROOT, image.image.name)
            # Nom du fichier sans extension
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            # Forcer extension .jpg
            new_filename = f"{base_name}.jpg"

            zip_file.write(image_path, arcname=new_filename)

    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=reglements_jpg.zip'

    return response


