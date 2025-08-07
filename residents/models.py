# residents/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
    # residents/models.py
from django.db import models
from django.utils import translation

from django.conf import settings
from django.db import models

class Resident(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Garçon'),
        ('F', 'Fille'),
    ]

    telephone = models.CharField(max_length=20, blank=True)
    date_naissance = models.DateField(blank=True, null=True)
    lieu_naissance = models.CharField(max_length=100, blank=True)
    nationalite = models.CharField(max_length=50, blank=True)
    universite = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    chambre = models.CharField(max_length=10, blank=True)
    genre = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)


# Fix the clashes by specifying unique related_name
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="resident_set",  # This is the fix
        related_query_name="resident",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="resident_user_permissions_set",  # This is the fix
        related_query_name="resident",
    )


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    



class Reservation(models.Model):
    ROOM_TYPE_CHOICES = [
        ('single', 'Simple'),
        ('double', 'Double'),
        ('triple', 'Triple'),
    ]

    GENDER_CHOICES = [
        ('M', 'Garçon'),
        ('F', 'Fille'),
    ]

    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('approved', 'Approuvée'),
        ('rejected', 'Refusée'),
        ('paid', 'Payée'),
        ('cancelled', 'Annulée'),
    ]

   
    resident = models.ForeignKey(User, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    roommate_preference = models.TextField(blank=True, help_text="Préférence de colocataire (étudiant, travailleur, ou nom connu)")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    payment_deadline = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"{self.resident.get_full_name()} - {self.get_room_type_display()}"

    class Meta:
        ordering = ['-requested_at']
        verbose_name = "Demande de réservation"
        verbose_name_plural = "Demandes de réservation"
    # Prix dynamique selon le type de chambre
    def get_price(self):
        prices = {'single': 350, 'double': 210, 'triple': 150}
        return prices.get(self.room_type, 0)

    def get_deposit(self):
        return self.get_price()  # Dépôt = 1 mois de loyer

    def __str__(self):
        return f"{self.resident.username} - {self.get_room_type_display()}"

    class Meta:
        verbose_name = "Demande de réservation"
        verbose_name_plural = "Demandes de réservation"


# residents/models.py


# residents/models.py


# residents/models.py


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente de vérification'),
        ('verified', 'Payé'),
        ('rejected', 'Rejeté'),
    ]

    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50)
    proof = models.ImageField(upload_to='payments/')
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(auto_now_add=True)  # ✅ Changé

    def __str__(self):
        return f"Paiement {self.get_status_display()} pour {self.reservation.resident}"

    def get_month_display(self):
        with translation.override(settings.LANGUAGE_CODE):  # Assure que la langue est 'fr'
         return self.created_at.strftime("%B %Y")  # Ex: Août 2025



# residents/models.py

class RoomPricing(models.Model):
    ROOM_TYPE_CHOICES = [
        ('single', 'Chambre individuelle'),
        ('double', 'Chambre double'),
        ('triple', 'Chambre triple'),
    ]

    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES, unique=True)
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    deposit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.get_room_type_display()} - {self.monthly_rent} DT"
    class Meta:
        verbose_name = "Tarification des chambres"
        verbose_name_plural = "Tarifications des chambres"    


# residents/models.py


class MonthlyPayment(models.Model):
    MONTH_CHOICES = [
        ('janvier', 'Janvier'),
        ('fevrier', 'Février'),
        ('mars', 'Mars'),
        ('avril', 'Avril'),
        ('mai', 'Mai'),
        ('juin', 'Juin'),
        ('juillet', 'Juillet'),
        ('aout', 'Août'),
        ('septembre', 'Septembre'),
        ('octobre', 'Octobre'),
        ('novembre', 'Novembre'),
        ('decembre', 'Décembre'),
    ]

    STATUS_CHOICES = [
        ('pending', 'En attente de vérification'),
        ('verified', 'Payé'),
        ('overdue', 'Non payé'),
    ]

    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    month = models.CharField(max_length=10, choices=MONTH_CHOICES)
    year = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    proof = models.ImageField(upload_to='payments/')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    paid_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reservation', 'month', 'year')
        ordering = ['-year', 'month']

    def __str__(self):
        return f"{self.month} {self.year} - {self.reservation.resident.username}"