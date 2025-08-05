# residents/management/commands/cancel_expired_reservations.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from residents.models import Reservation

class Command(BaseCommand):
    help = 'Annule toutes les réservations approuvées dont le délai de paiement est expiré'

    def handle(self, *args, **options):
        now = timezone.now()
        # Trouver les réservations approuvées avec deadline dépassée
        expired_reservations = Reservation.objects.filter(
            status='approved',
            payment_deadline__lt=now
        )
        
        count = expired_reservations.count()
        if count > 0:
            # Changer leur statut à 'cancelled'
            expired_reservations.update(status='cancelled')
            self.stdout.write(
                self.style.SUCCESS(f'Successfully cancelled {count} reservation(s).')
            )
        else:
            self.stdout.write('No expired reservations found.')