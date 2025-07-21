from django.db import models
from django.contrib.auth.models import AbstractUser

class Resident(AbstractUser):
    telephone = models.CharField(max_length=20, blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)
    lieu_naissance = models.CharField(max_length=100, blank=True, null=True)
    nationalite = models.CharField(max_length=50, blank=True, null=True)
    universite = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    chambre = models.CharField(max_length=10, blank=True, null=True)

    # Résoudre les conflits
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='residents_user_set',  # Changé ici
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='residents_permission_set',  # Changé ici
        related_query_name='user'
    )