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
        order = Order.objects.get(
            id=serializer.validated_data['order_id'],
            user=request.user
        )

        if settings.PAYMENT_USE_MOCK:
            # ==== MODO MOCK ====
            token = f"MOCK-{uuid.uuid4()}"
            url   = f"http://localhost:8000/mock-pay/{token}"
            trans = PaymentTransaction.objects.create(
                order=order,
                user=request.user,
                amount=order.total,
                token=token,
                url=url,
                status='PENDING'
            )
            return Response(
                {"token": trans.token, "url": trans.url},
                status=status.HTTP_201_CREATED
            )

        # ==== MODO REAL (descomenta y adapta) ====
        # resp = requests.post( ... )
        # result = resp.json()
        # trans = PaymentTransaction.objects.create( ... )
        # return Response({"token": trans.token, "url": trans.url}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def confirm(self, request):
        """
        Confirma la transacción (mock o real).
        """
        token = request.data.get("token")
        if not token:
            return Response({"detail": "Falta token"}, status=status.HTTP_400_BAD_REQUEST)

        trans = PaymentTransaction.objects.get(token=token, user=request.user)
        if settings.PAYMENT_USE_MOCK:
            # ==== MODO MOCK ====
            trans.status = 'COMPLETED'
            trans.save()
            return Response({"status": trans.status}, status=status.HTTP_200_OK)

        # ==== MODO REAL (descomenta y adapta) ====
        # resp = requests.put( ... )
        # result = resp.json()
        # trans.status = result.get("status", "")
        # trans.save()
        # return Response(result)

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """
        Consulta el estado actual (mock o real).
        """
        trans = PaymentTransaction.objects.get(pk=pk, user=request.user)
        if settings.PAYMENT_USE_MOCK:
            return Response({"token": trans.token, "status": trans.status})

        # ==== MODO REAL (descomenta y adapta) ====
        # resp = requests.get( ... )
        # return Response(resp.json())

    def retrieve(self, request, pk=None):
        """
        Detalle guardado (idéntico en mock o real).
        Mapeado automáticamente como GET /api/pagos/{pk}/
        """
        trans = PaymentTransaction.objects.get(pk=pk, user=request.user)
        serializer = PaymentTransactionSerializer(trans)
        return Response(serializer.data)