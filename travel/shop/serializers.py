from rest_framework import serializers
from .models import Order, Ticket
from auth_.serializers import MainUserSerializer
from payment.models import Payment


class OrderPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('event', 'quantity', 'status')
        write_only_fields = ('status', )

    def purchase(self):
        order = Order(**self.validated_data)
        order.user = self.context['request'].user
        order.save()
        payment = Payment.objects.from_order(order=order)
        return {'paybox_url': payment.get_payment_url()}


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

    order = OrderPurchaseSerializer()
