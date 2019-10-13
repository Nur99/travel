from rest_framework.decorators import action, api_view
from rest_framework import mixins, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from auth_.models import Activation, MainUser
from auth_.message import send_html
from auth_.token import get_token
from auth_.serializers import (ActivationSerializer, EmailSerializer,
                               RegistrationSerializer, MainUserSerializer,
                               LoginSerializer)
from utils import messages


class ActivationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Activation.objects.all()
    http_method_names = ['post', 'get']
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action == 'create':
            return EmailSerializer
        return ActivationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        activation = serializer.create_activation()
        return Response({'activation': ActivationSerializer(activation).data})

    @action(methods=['get'], detail=True)
    def resend_msg(self, request, pk=None):
        activation = self.get_object()
        activation.is_valid(raise_exception=True)
        send_html(activation, request)
        return Response({'activation': ActivationSerializer(activation).data})


@api_view(['GET'])
def activate(request, uuid):
    try:
        activation = Activation.objects.get(uuid=uuid)
    except Activation.DoesNotExist:
        raise ValidationError(messages.LINK_INVALID)
    activation.is_valid(raise_exception=True)
    serializer = RegistrationSerializer(data={
        'email': activation.email,
        'password': activation.password,
        'full_name': activation.full_name})
    serializer.is_valid(raise_exception=True)
    user = serializer.complete(activation)
    return Response({'user': MainUserSerializer(user).data})


class UserViewSet(viewsets.GenericViewSet):
    queryset = MainUser.objects.all()
    http_method_names = ['post']
    permission_classes = (AllowAny,)
    serializer_class = MainUserSerializer

    @action(methods=['post'], detail=False)
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = get_token(user)
        return Response({'user': MainUserSerializer(user).data,
                         'token': token})
