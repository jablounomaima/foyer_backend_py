# residents/admin.py
<<<<<<< HEAD

from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.html import format_html
from django.contrib import messages

from .models import Reservation, Payment, RoomPricing, MonthlyPayment
from .forms import PaymentAdminForm  # Assurez-vous que ce formulaire existe


# =================== ADMIN RESERVATION ===================
=======
from datetime import timezone
from pyexpat.errors import messages
from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.utils.html import format_html

from residents.forms import PaymentAdminForm
from .models import Payment, Reservation
>>>>>>> e895eca4c3f584252cf6d671c0ac4c79addbddef

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
<<<<<<< HEAD
    
=======
>>>>>>> e895eca4c3f584252cf6d671c0ac4c79addbddef
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
<<<<<<< HEAD
=======
        from django.utils import timezone
        import datetime
>>>>>>> e895eca4c3f584252cf6d671c0ac4c79addbddef
        now = timezone.now()
        count = 0
        for reservation in queryset:
            if reservation.status == 'pending':
                reservation.status = 'approved'
                reservation.approved_at = now
<<<<<<< HEAD
                reservation.payment_deadline = now + timezone.timedelta(days=3)
=======
                reservation.payment_deadline = now + datetime.timedelta(days=3)
>>>>>>> e895eca4c3f584252cf6d671c0ac4c79addbddef
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

<<<<<<< HEAD

# =================== ADMIN PAYMENT ===================

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('display_resident', 'amount', 'method', 'status', 'created_at', 'proof_preview', 'admin_actions')
    list_filter = ('status', 'method', 'created_at')
    search_fields = ('reservation__resident__username', 'reservation__resident__first_name', 'reservation__resident__last_name')
    readonly_fields = ('created_at', 'updated_at', 'proof_preview')

    @admin.display(description='Résident')
    def display_resident(self, obj):
        return f"{obj.resident.get_full_name()} ({obj.resident.username})"
=======
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
>>>>>>> e895eca4c3f584252cf6d671c0ac4c79addbddef

    @admin.display(description='Aperçu preuve')
    def proof_preview(self, obj):
        if obj.proof:
<<<<<<< HEAD
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" width="100" height="60" style="object-fit: cover;"></a>',
                obj.proof.url, obj.proof.url
            )
        return "❌ Aucune"

=======
            return format_html('<a href="{}" target="_blank"><img src="{}" width="100" height="60" style="object-fit: cover;"></a>', obj.proof.url, obj.proof.url)
        return "❌ Aucune"
    
>>>>>>> e895eca4c3f584252cf6d671c0ac4c79addbddef
    @admin.display(description='Actions')
    def admin_actions(self, obj):
        if obj.status == 'pending':
            return format_html(
                '<a class="button" href="{}">Valider</a>',
                f"{obj.id}/verify/"
            )
        return "-"

<<<<<<< HEAD
=======

>>>>>>> e895eca4c3f584252cf6d671c0ac4c79addbddef
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
<<<<<<< HEAD
            self.message_user(request, f"Paiement validé pour {payment.resident.get_full_name()}.")
        return self.response_change(request, payment)


# =================== ADMIN TARIFICATION ===================
=======
            messages.success(request, f"Paiement validé pour {payment.reservation}.")
        return self.response_change(request, payment)

   

   

    
    

    

   
    


    # residents/admin.py
from django.contrib import admin
from .models import RoomPricing
>>>>>>> e895eca4c3f584252cf6d671c0ac4c79addbddef

@admin.register(RoomPricing)
class RoomPricingAdmin(admin.ModelAdmin):
    list_display = ('get_room_type_display', 'monthly_rent', 'deposit')
    list_editable = ('monthly_rent', 'deposit')
    list_filter = ('room_type',)
    readonly_fields = ()

    def get_room_type_display(self, obj):
        return obj.get_room_type_display()
<<<<<<< HEAD
    get_room_type_display.short_description = 'Type de chambre'


# =================== ADMIN PAIEMENT MENSUEL ===================

@admin.register(MonthlyPayment)
class MonthlyPaymentAdmin(admin.ModelAdmin):
    list_display = ('resident', 'display_month', 'year', 'amount', 'status', 'proof_preview', 'paid_at')
    list_filter = ('status', 'month', 'year', 'reservation__resident')
    search_fields = ('reservation__resident__first_name', 'reservation__resident__last_name')

    @admin.display(description='Résident')
    def resident(self, obj):
        return obj.reservation.resident.get_full_name()

    @admin.display(description='Mois')
    def display_month(self, obj):
        return obj.get_month_display()

    @admin.display(description='Preuve')
    def proof_preview(self, obj):
        if obj.proof:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" width="50" height="50" style="object-fit: cover;"></a>',
                obj.proof.url, obj.proof.url
            )
        return "❌"

    actions = ['verify_payments']

    @admin.action(description='Marquer comme payé')
    def verify_payments(self, request, queryset):
        queryset.update(status='verified')
        self.message_user(request, "Paiements validés.")

 # =================== ADMIN UTILISATEUR (Resident) ===================
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Resident

# Désenregistrer User SANS erreur si ce n'est pas encore enregistré
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass  # Le modèle User n'était pas enregistré, pas de problème

@admin.register(Resident)
class CustomResidentAdmin(UserAdmin):
    # ✅ Bon : concaténation de tuples
    list_display = UserAdmin.list_display + ('telephone',)

    # Pour fieldsets, on travaille avec des listes (car mutable)
    fieldsets = list(UserAdmin.fieldsets)
    fieldsets[1][1]['fields'] = list(fieldsets[1][1]['fields']) + ['telephone']

    search_fields = UserAdmin.search_fields + ('telephone',)
    list_filter = UserAdmin.list_filter + ('telephone',)



# residents/admin.py
from django.contrib import admin
from .models import ReglementImage



#  Partie Admin : Gestion des images du règlement intérieur
from django.contrib import admin
from django.utils.html import format_html
from .models import ReglementImage

# residents/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import ReglementImage


@admin.register(ReglementImage)
class ReglementImageAdmin(admin.ModelAdmin):
    list_display = ('preview_thumbnail', 'titre', 'ordre', 'mis_en_ligne', 'actions_column')
    list_editable = ('titre', 'ordre', 'mis_en_ligne')  # ✅ 'titre' est ici → bien
    list_display_links = ('preview_thumbnail', )
    list_filter = ('mis_en_ligne',)
    search_fields = ('titre',)
    ordering = ['ordre']
    readonly_fields = ('image_preview', 'file_info')

    # ✅ Supprimez cette ligne si elle existe :
    # actions = ...

    # Ou si vous voulez garder les actions par défaut (comme "Supprimer sélectionné"), laissez vide ou supprimez
    # Django utilise les actions par défaut automatiquement

    fieldsets = (
        ('Image', {
            'fields': ('image_preview', 'image', 'file_info')
        }),
        ('Informations', {
            'fields': ('titre', 'ordre', 'mis_en_ligne')
        }),
    )

    def preview_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 6px;">',
                obj.image.url
            )
        return format_html(
            '<div style="width:50px; height:50px; background:#f0f0f0; display:flex; align-items:center; justify-content:center; border-radius:6px;">📷</div>'
        )
    preview_thumbnail.short_description = "Aperçu"

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 300px; max-width: 100%; border-radius: 8px; border: 1px solid #ddd;">',
                obj.image.url
            )
        return "❌ Aucune image"
    image_preview.short_description = "Aperçu complet"

    def file_info(self, obj):
        if obj.image:
            import os
            file_size = os.path.getsize(obj.image.path)
            size_display = f"{file_size // 1024} Ko" if file_size < 1024*1024 else f"{file_size / (1024*1024):.1f} Mo"
            return format_html(
                "<strong>Nom du fichier :</strong> {}<br><strong>Taille :</strong> {}",
                os.path.basename(obj.image.name),
                size_display
            )
        return "Aucune information"
    file_info.short_description = "Informations sur le fichier"





    def preview_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 6px;">',
                obj.image.url
            )
        return format_html(
            '<div style="width:50px; height:50px; background:#f0f0f0; display:flex; align-items:center; justify-content:center; border-radius:6px;">📷</div>'
        )
    preview_thumbnail.short_description = "Aperçu"

    def actions_column(self, obj):
        return format_html(
            '<a class="btn btn-sm btn-info" href="/admin/residents/reglementimage/{}/change/">Modifier</a>',
            obj.pk
        )
    actions_column.short_description = "Actions"










def image_preview(self, obj):
    if obj.image:
        return format_html('<img src="{}" style="max-height: 50px;">', obj.image.url)
    return "Aucune image"
=======
    get_room_type_display.short_description = 'Type de chambre'
>>>>>>> e895eca4c3f584252cf6d671c0ac4c79addbddef
