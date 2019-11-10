from django.utils.decorators import method_decorator
from utils import constants
from utils.decorators import response_wrapper
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from .serializers import (PaymentSerializer, PaymentListSerializer,
                          PayTicketSerializer)
from .models import Payment


@method_decorator(response_wrapper(), name='dispatch')
class PaymentViewSet(viewsets.ReadOnlyModelViewSet, viewsets.GenericViewSet):
    queryset = Payment.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = PaymentSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return PaymentListSerializer
        elif self.action == 'pay':
            return PayTicketSerializer
        return self.serializer_class

    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.filter(user=self.request.user,
                                   status=constants.SUCCESS)
        return queryset

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def pay(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.pay(pk)
        return Response(result)


class CardDetail(viewsets.generics.RetrieveAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = (AllowAny,)
    template_name = 'payment.html'
    serializer_class = PayTicketSerializer

    def get(self, request, id):
        instance = Payment.objects.get(id=id)
        return Response({'payment': id,
                         'total_price': instance.total_price})
