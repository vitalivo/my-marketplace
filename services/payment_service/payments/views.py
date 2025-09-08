from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentCreateSerializer, PaymentRetrieveSerializer

class PaymentViewSet(viewsets.GenericViewSet,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin):
    """
    * `list` – список всех платежей текущего пользователя.
    * `retrieve` – детали отдельного платежа.
    * `create` – создать Stripe Checkout Session и вернуть URL.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentRetrieveSerializer

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return PaymentCreateSerializer
        return PaymentRetrieveSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data, status=status.HTTP_201_CREATED)