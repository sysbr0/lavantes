from django.contrib import admin
from .models import  clints  , ClintPayment
# Register your models here.



import uuid


from django.utils.html import format_html

@admin.register(clints)
class clintsAdmin(admin.ModelAdmin):
    list_display = ('name', 'tex', 'email', 'profile_image', 'balance', 'is_company')
    list_filter = ('balance', 'is_company', 'created_by')
    search_fields = ('name', 'tex', 'email', 'company', 'number')
    ordering = ('name',)
    readonly_fields = ('balance', 'token', 'total_paied', 'total_buy')
    actions = ['mark_as_company']

    def mark_as_company(self, request, queryset):
        queryset.update(is_company=True)
        self.message_user(request, f"{queryset.count()} clients marked as companies.")
    mark_as_company.short_description = "Mark selected clients as companies"

    def profile_image(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="100" />', obj.profile_image.url)
        return 'No image'
    profile_image.short_description = 'Profile Image'




@admin.register(ClintPayment)
class ClintPaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_token', 'clint', 'amount', 'date', 'source', 'note')
    list_filter = ('source', 'clint', 'date')
    search_fields = ('clint__name', 'payment_token', 'note')
    readonly_fields = ('payment_token', 'date')
    ordering = ('-date',)

    def save_model(self, request, obj, form, change):
        # Optionally override save_model to perform actions before saving
        if not obj.payment_token:
            obj.payment_token = uuid.uuid4()
        super().save_model(request, obj, form, change)