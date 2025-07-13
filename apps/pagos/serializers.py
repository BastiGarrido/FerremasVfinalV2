from rest_framework import serializers
from .models import PaymentTransaction

class PaymentInitSerializer(serializers.Serializer):
    """
    Recibe el ID de un pedido para iniciar la transacción.
    """
    order_id = serializers.IntegerField()

class PaymentTransactionSerializer(serializers.ModelSerializer):
    """
    Serializador para ver el detalle de la transacción almacenada.
    """
    class Meta:
        model = PaymentTransaction
        fields = [
            'id',
            'order',
            'amount',
            'token',
            'url',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'amount',
            'token',
            'url',
            'status',
            'created_at',
            'updated_at',
        ]