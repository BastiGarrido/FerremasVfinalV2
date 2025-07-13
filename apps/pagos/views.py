from django.shortcuts import render
import uuid
from django.conf import settings
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import PaymentTransaction
from .serializers import PaymentInitSerializer, PaymentTransactionSerializer
from apps.pedidos.models import Order

class PaymentViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def initiate(self, request):
        """
        Inicia la transacción (mock o real).
        """
        serializer = PaymentInitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = request.user.profile
        order = Order.objects.get(
            id=serializer.validated_data['order_id'],
            user=profile
        )
        if settings.PAYMENT_USE_MOCK:
            token = f"MOCK-{uuid.uuid4()}"
            url   = f"http://localhost:8000/mock-pay/{token}"
            trans = PaymentTransaction.objects.create(
                order=order,
                user=profile,
                amount=order.total,
                token=token,
                url=url,
                status='PENDING'
            )
            return Response({"token": trans.token, "url": trans.url}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def confirm(self, request):
        """
        Confirma la transacción (mock).
        """
        token = request.data.get("token")
        if not token:
            return Response({"detail": "Falta token"}, status=status.HTTP_400_BAD_REQUEST)
        trans = PaymentTransaction.objects.get(token=token, user=request.user.profile)
        trans.status = 'COMPLETED'
        trans.save()
        return Response({"status": trans.status}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """
        Consulta el estado actual.
        """
        trans = PaymentTransaction.objects.get(pk=pk, user=request.user.profile)
        return Response({"token": trans.token, "status": trans.status})

    # Método retrieve por defecto (sin @action) para detalle
    def retrieve(self, request, pk=None):
        """
        Detalle guardado.
        """
        trans = PaymentTransaction.objects.get(pk=pk, user=request.user.profile)
        ser   = PaymentTransactionSerializer(trans)
        return Response(ser.data)