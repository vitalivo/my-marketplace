from rest_framework import serializers
from .models import Payment
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


class PaymentCreateSerializer(serializers.Serializer):
    """Создаёт Stripe Checkout Session и сохраняет запись в БД."""
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=10, default='usd')
    success_url = serializers.URLField()
    cancel_url = serializers.URLField()

    def create(self, validated_data):
        user = self.context['request'].user
        amount_cents = int(validated_data['amount'] * 100)

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': validated_data['currency'],
                    'product_data': {'name': 'Marketplace purchase'},
                    'unit_amount': amount_cents,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=validated_data['success_url'],
            cancel_url=validated_data['cancel_url'],
            metadata={'user_id': str(user.id)},
        )

        payment = Payment.objects.create(
            user=user,
            stripe_session_id=session.id,
            amount=validated_data['amount'],
            currency=validated_data['currency'],
        )
        return {'checkout_url': session.url, 'payment_id': payment.id}


class PaymentRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'user', 'stripe_session_id', 'amount',
                  'currency', 'completed', 'created_at')
        read_only_fields = fields