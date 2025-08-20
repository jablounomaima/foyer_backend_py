from django import forms
from .models import Resident
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Payment
# residents/forms.py

from django import forms
from .models import Reservation
from django.contrib.auth import get_user_model
# Utilisez get_user_model() pour obtenir le modèle utilisateur actuel
Resident = get_user_model()

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['room_type', 'gender', 'roommate_preference']
        widgets = {
            'roommate_preference': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Ex: Étudiant en médecine, ou "Je souhaite partager avec Ahmed"'
            })
        }

    def __init__(self, *args, **kwargs):
        # Permet de passer l'utilisateur connecté
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        # Associe automatiquement le résident
        reservation = super().save(commit=False)
        if self.user:
            reservation.resident = self.user
        if commit:
            reservation.save()
        return reservation










class ResidentSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
     # Champs supplémentaires
    telephone = forms.CharField(max_length=20, required=False, label="Téléphone")
    date_naissance = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Date de naissance")
    lieu_naissance = forms.CharField(max_length=100, required=False, label="Lieu de naissance")
    nationalite = forms.CharField(max_length=50, required=False, label="Nationalité")
    universite = forms.CharField(max_length=100, required=False, label="Université")
    photo = forms.ImageField(required=False, label="Photo de profil")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 
                  'telephone', 'date_naissance', 'lieu_naissance', 
                  'nationalite', 'universite', 'photo', 
                  'password1', 'password2')


class PaymentAdminForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount']  # Champ modifiable par l'admin

# residents/forms.py
from django import forms
from .models import Payment

# residents/forms.py
from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['method', 'proof', 'notes']
        widgets = {
            'proof': forms.FileInput(attrs={'accept': 'image/*'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Référence de transaction, nom sur le compte, etc.'})
        } 



 # residents/forms.py
from django import forms
from .models import Resident

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Resident
        fields = [
            'first_name', 'last_name', 'email',
            'telephone', 'date_naissance', 'lieu_naissance',
            'nationalite', 'universite', 'photo'
        ]
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }  



class ResidentCreationForm(UserCreationForm):
    telephone = forms.CharField(
        max_length=20,
        required=False,
        label="Téléphone",
        widget=forms.TextInput(attrs={'placeholder': '+212612345678'})
    )

    class Meta:
        model = Resident  # ✅ Pas User, ni auth.User
        fields = ('username', 'first_name', 'last_name', 'email', 'telephone', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.telephone = self.cleaned_data['telephone']
        if commit:
            user.save()
        return user