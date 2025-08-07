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
from .forms import PaymentForm
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

def signup_view(request):
    if request.method == 'POST':
        form = ResidentSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('dashboard')
    else:
        form = ResidentSignupForm()
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

    # Vérifiez s'il existe déjà un paiement
    if hasattr(reservation, 'payment'):
        messages.warning(request, "Un paiement a déjà été soumis pour cette réservation. En attente de vérification.")
        return redirect('reservation_status')

    if request.method == 'POST':
        method = request.POST.get('method')
        proof = request.FILES.get('proof')
        notes = request.POST.get('notes')

        if method and proof:
            Payment.objects.create(
                reservation=reservation,
                amount=reservation.get_price() + reservation.get_deposit(),
                method=method,
                proof=proof,
                notes=notes,
                status='pending'
            )
            messages.success(request, "Votre paiement a été envoyé. En attente de vérification.")
            return redirect('reservation_status')
        else:
            messages.error(request, "Veuillez remplir tous les champs.")

    return render(request, 'residents/make_payment.html', {'reservation': reservation})
# residents/views.py
# residents/views.py
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



@login_required
def reglements(request):
    return render(request, 'residents/reglements.html')





# residents/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Reservation, Payment
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
            payment.amount = reservation.get_price() + reservation.get_deposit()
            payment.save()
            messages.success(request, "Votre paiement a été envoyé. En attente de vérification.")
            return redirect('reservation_status')
        else:
            messages.error(request, "Veuillez remplir tous les champs.")
    else:
        form = PaymentForm()

    return render(request, 'residents/make_payment.html', {'reservation': reservation, 'form': form})
    # residents/views.py

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


@login_required
def make_monthly_payment(request, reservation_id, month, year):
    reservation = get_object_or_404(Reservation, id=reservation_id, resident=request.user)
    
    # Convertir le slug en nom de mois
    month_map = {
        'janvier': 'janvier', 'février': 'fevrier', 'mars': 'mars',
        'avril': 'avril', 'mai': 'mai', 'juin': 'juin',
        'juillet': 'juillet', 'août': 'aout', 'septembre': 'septembre',
        'octobre': 'octobre', 'novembre': 'novembre', 'décembre': 'decembre'
    }
    month_key = next((k for k, v in month_map.items() if v == month), None)
    if not month_key:
        messages.error(request, "Mois invalide.")
        return redirect('payment_history')

    year = int(year)

    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            pricing = RoomPricing.objects.get(room_type=reservation.room_type)
            payment = form.save(commit=False)
            payment.reservation = reservation
            payment.month = month_key
            payment.year = year
            payment.amount = pricing.monthly_rent
            payment.status = 'pending'
            payment.save()
            messages.success(request, f"Paiement de {month_key} {year} envoyé. En attente de vérification.")
            return redirect('payment_history')
    else:
        form = PaymentForm()

    return render(request, 'residents/make_monthly_payment.html', {
        'form': form,
        'month': month_key.capitalize(),
        'year': year
    })