# residents/admin.py
from datetime import timezone
from pyexpat.errors import messages
from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.utils.html import format_html

from residents.forms import PaymentAdminForm
from .models import Payment, Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        'display_resident',
        'room_type',
        'gender',
        'status',
        'requested_at',
        'payment_deadline',
        'admin_actions',
    )
    list_filter = ('status', 'room_type', 'gender', 'requested_at')
    search_fields = ('resident__first_name', 'resident__last_name', 'resident__username')
    readonly_fields = ('requested_at', 'approved_at')
    actions = ['approve_reservations', 'reject_reservations']

    @admin.display(description='Résident')
    def display_resident(self, obj):
        return f"{obj.resident.get_full_name()} ({obj.resident.username})"

    @admin.display(description='Actions')
    def admin_actions(self, obj):
        if obj.status == 'pending':
            return format_html(
                '<a class="button" href="{}">Approuver</a> | <a class="button" href="{}">Refuser</a>',
                f"{obj.id}/approve/",
                f"{obj.id}/reject/"
            )
        return "-"

    @admin.action(description='Approuver les demandes sélectionnées')
    def approve_reservations(self, request, queryset):
        from django.utils import timezone
        import datetime
        now = timezone.now()
        count = 0
        for reservation in queryset:
            if reservation.status == 'pending':
                reservation.status = 'approved'
                reservation.approved_at = now
                reservation.payment_deadline = now + datetime.timedelta(days=3)
                reservation.save()
                count += 1
        if count > 0:
            self.message_user(request, f"{count} demande(s) approuvée(s).")

    @admin.action(description='Refuser les demandes sélectionnées')
    def reject_reservations(self, request, queryset):
        count = 0
        for reservation in queryset:
            if reservation.status == 'pending':
                reservation.status = 'rejected'
                reservation.save()
                count += 1
        if count > 0:
            self.message_user(request, f"{count} demande(s) refusée(s).")

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('<int:reservation_id>/approve/', self.admin_site.admin_view(self.approve_view), name='reservation-approve'),
            path('<int:reservation_id>/reject/', self.admin_site.admin_view(self.reject_view), name='reservation-reject'),
        ]
        return custom_urls + urls

    def approve_view(self, request, reservation_id):
        reservation = self.get_object(request, reservation_id)
        if reservation and reservation.status == 'pending':
            reservation.status = 'approved'
            reservation.approved_at = timezone.now()
            reservation.payment_deadline = timezone.now() + timezone.timedelta(days=3)
            reservation.save()
            self.message_user(request, f"✅ Approuvé : {reservation.resident.get_full_name()}")
        return self.response_change(request, reservation)

    def reject_view(self, request, reservation_id):
        reservation = self.get_object(request, reservation_id)
        if reservation and reservation.status == 'pending':
            reservation.status = 'rejected'
            reservation.save()
            self.message_user(request, f"❌ Refusé : {reservation.resident.get_full_name()}")
        return self.response_change(request, reservation)

# residents/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Payment

# residents/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'amount', 'method', 'status', 'created_at', 'proof_preview')
    list_filter = ('status', 'method', 'created_at')
    search_fields = ('reservation__resident__username', 'reservation__resident__first_name')
       # ✅ Utilisez get_readonly_fields() pour ajouter des méthodes
    def get_readonly_fields(self, request, obj=None):
        return ['created_at', 'updated_at'] + (['proof_preview'] if obj else [])

    @admin.display(description='Aperçu preuve')
    def proof_preview(self, obj):
        if obj.proof:
            return format_html('<a href="{}" target="_blank"><img src="{}" width="100" height="60" style="object-fit: cover;"></a>', obj.proof.url, obj.proof.url)
        return "❌ Aucune"
    
    @admin.display(description='Actions')
    def admin_actions(self, obj):
        if obj.status == 'pending':
            return format_html(
                '<a class="button" href="{}">Valider</a>',
                f"{obj.id}/verify/"
            )
        return "-"


    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('<int:payment_id>/verify/', self.admin_site.admin_view(self.verify_payment), name='payment-verify'),
        ]
        return custom_urls + urls

    def verify_payment(self, request, payment_id):
        payment = get_object_or_404(Payment, id=payment_id)
        if payment.status == 'pending':
            payment.status = 'verified'
            payment.save()
            messages.success(request, f"Paiement validé pour {payment.reservation}.")
        return self.response_change(request, payment)

   

   

    
    

    

   
    


    # residents/admin.py
from django.contrib import admin
from .models import RoomPricing

@admin.register(RoomPricing)
class RoomPricingAdmin(admin.ModelAdmin):
    list_display = ('get_room_type_display', 'monthly_rent', 'deposit')
    list_editable = ('monthly_rent', 'deposit')
    list_filter = ('room_type',)
    readonly_fields = ()

    def get_room_type_display(self, obj):
        return obj.get_room_type_display()
    get_room_type_display.short_description = 'Type de chambre'