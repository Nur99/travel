from rest_framework import serializers
from .models import Order


class OrderPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        depth = 2

    # def purchase(self):
    #     order = Order(**self.validated_data)
    #     order.user = self.context['request'].user
    #     order.save()
    #     payment = Payment.objects.from_order(order=order)
    #     return {'paybox_url': payment.get_paybox_url()}
    #
