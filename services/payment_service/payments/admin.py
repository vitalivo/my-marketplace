from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'currency', 'completed', 'created_at')
    list_filter = ('completed', 'currency')
    search_fields = ('stripe_session_id', 'user__username')