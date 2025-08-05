from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('resident', 'room_type', 'gender', 'status', 'requested_at', 'payment_deadline')
    list_filter = ('status', 'room_type', 'gender', 'requested_at')
    search_fields = ('resident__username', 'resident__first_name', 'resident__last_name')
    actions = ['approve_reservations']

    @admin.action(description='Approuver les réservations sélectionnées')
    def approve_reservations(self, request, queryset):
        from datetime import timedelta
        from django.utils import timezone

        for reservation in queryset:
            if reservation.status == 'pending':
                reservation.status = 'approved'
                reservation.approved_at = timezone.now()
                reservation.payment_deadline = timezone.now() + timedelta(days=3)  # 3 jours pour payer
                reservation.save()