from rest_framework import serializers
from shop.serializers import TicketSerializer, OrderPurchaseSerializer
from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'created_at', 'total_price',
                  'order', 'description', 'status')

    order = OrderPurchaseSerializer()

    def to_representation(self, instance):
        representation = super(PaymentSerializer, self).to_representation(instance)  # noqa
        representation['tickets'] = TicketSerializer(
            instance.order.tickets.all(), many=True).data
        return representation


class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'created_at', 'quantity', 'price', 'total_price',
                  'description', 'status')


class PayTicketSerializer(serializers.Serializer):
    name_on_card = serializers.CharField(max_length=100)
    card_number = serializers.IntegerField()
    expiration = serializers.CharField(max_length=10)
    cvv = serializers.IntegerField()

    def pay(self, pk):
        p = Payment.objects.get(id=pk)
        p.card = self.validated_data['card_number']
        p.save()
        p.success()
        return {'result': 'success'}

