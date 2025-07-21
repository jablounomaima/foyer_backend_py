from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def dashboard(request):
    return render(request, 'residents/dashboard.html')

@login_required
def profil(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profil')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'residents/profil.html', {'form': form})

@login_required
def chambre(request):
    return render(request, 'residents/chambre.html')

@login_required
def demandes(request):
    return render(request, 'residents/demandes.html')



@login_required
def annonces(request):
    return render(request, 'residents/annonces.html')


@login_required
def paiement(request):
    return render(request, 'residents/paiements.html')


@login_required
def reglements(request):
    return render(request, 'residents/reglements.html')





