# residents/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


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
        ('paid', 'Payée'),
        ('cancelled', 'Annulée'),
    ]

    resident = models.ForeignKey(User, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    roommate_preference = models.TextField(blank=True, help_text="Étudiant, travailleur, ou nom d'une personne connue")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    payment_deadline = models.DateTimeField(null=True, blank=True)

    # Prix dynamique selon le type de chambre
    def get_price(self):
        prices = {'single': 35000, 'double': 25000, 'triple': 20000}
        return prices.get(self.room_type, 0)

    def get_deposit(self):
        return self.get_price()  # Dépôt = 1 mois de loyer

    def __str__(self):
        return f"{self.resident.username} - {self.get_room_type_display()}"

    class Meta:
        ordering = ['-requested_at']