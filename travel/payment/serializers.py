from rest_framework import serializers
from shop.serializers import TicketSerializer, OrderPurchaseSerializer
from payment.models import Payment
from utils import constants


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'created_at', 'quantity', 'price', 'total_price', 'order', 'description',
                  'status')

    order = OrderPurchaseSerializer()

    def to_representation(self, instance):
        representation = super(PaymentSerializer, self).to_representation(instance)
        representation['tickets'] = TicketSerializer(instance.order.tickets.all(),
                                                         many=True).data
        return representation


class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'created_at', 'quantity', 'price', 'total_price', 'description', 'status')
