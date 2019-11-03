from django.utils.decorators import method_decorator
from utils import constants, paybox, messages
from utils.decorators import response_wrapper, verify_paybox
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import PaymentSerializer, PaymentListSerializer
from .models import CallBack, Payment


@method_decorator(response_wrapper(), name='dispatch')
class PayboxViewSet(viewsets.ViewSet):
    queryset = Payment.objects.all()
    permission_classes = (AllowAny,)

    @action(methods=['post'], detail=False)
    @method_decorator(verify_paybox())
    def check(self, request):
        CallBack.objects.create(meta_text=str(request.META), body_text=request.body,
                                get_text=request.GET, pb_result=CallBack.CHECK)
        return Response()

    @action(methods=['post'], detail=False)
    @method_decorator(verify_paybox())
    def result(self, request):
        CallBack.objects.create(meta_text=str(request.META), body_text=request.body,
                                get_text=request.GET, result=CallBack.RESULT)
        body = paybox.parse_body(request.body)
        try:
            payment = self.queryset.get(id=body['pg_order_id'])
        except Payment.DoesNotExist:
            raise ValidationError(messages.NOT_FOUND)
        if body['pg_result'] == '1':
            payment.success(body)
        else:
            payment.fail(body)
        return Response()

    @action(methods=['post'], detail=False)
    @method_decorator(verify_paybox())
    def refund(self, request):
        CallBack.objects.create(meta_text=str(request.META), body_text=request.body,
                                get_text=request.GET, result=CallBack.REFUND)
        return Response({'refund': 'refund'})

    @action(methods=['post'], detail=False)
    @method_decorator(verify_paybox())
    def capture(self, request):
        CallBack.objects.create(meta_text=str(request.META), body_text=request.body,
                                get_text=request.GET, result=CallBack.CAPTURE)
        return Response({'capture': 'capture'})

    @action(methods=['post'], detail=False)
    @method_decorator(verify_paybox())
    def success(self, request):
        CallBack.objects.create(meta_text=str(request.META), body_text=request.body,
                                get_text=request.GET, result=CallBack.SUCCESS)
        return Response({'success': 'success'})

    @action(methods=['post'], detail=False)
    @method_decorator(verify_paybox())
    def failure(self, request):
        CallBack.objects.create(meta_text=str(request.META), body_text=request.body,
                                get_text=request.GET, result=CallBack.FAILURE)
        return Response({'failure': 'failure'})


@method_decorator(response_wrapper(), name='dispatch')
class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = PaymentSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return PaymentListSerializer
        return self.serializer_class

    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.filter(user=self.request.user, status=constants.SUCCESS)
        return queryset
