from django.db import models
from django.conf import settings

class Payment(models.Model):
    """
    Хранит информацию о платеже, созданном через Stripe Checkout.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    stripe_session_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)   # в выбранной валюте
    currency = models.CharField(max_length=10, default='usd')
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment {self.id} – {self.amount} {self.currency}"