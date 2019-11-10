from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import (OrderPurchaseSerializer, TicketSerializer)
from .models import Order, Ticket
from utils.decorators import response_wrapper


@method_decorator(response_wrapper(), name='dispatch')
class OrderViewSet(viewsets.GenericViewSet):
    queryset = Order.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderPurchaseSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset

    @action(methods=['post'], detail=False)
    def purchase(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.purchase()
        return Response(result)


@method_decorator(response_wrapper(), name='dispatch')
class TicketViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.queryset.filter(order__user=self.request.user)
