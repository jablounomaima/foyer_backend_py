from django import forms
from .models import Resident

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Resident
        fields = [
            'first_name',
            'last_name',
            'email',
            'telephone',
            'date_naissance',
            'lieu_naissance',
            'nationalite',
            'universite',
            'photo',  # ✅ Important !
        ]