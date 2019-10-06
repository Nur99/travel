from django.shortcuts import render
from rest_framework.decorators import action, api_view
from rest_framework import mixins, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from auth_.models import Activation
from auth_.serializers import (ActivationSerializer, EmailSerializer,
                               RegistrationSerializer, MainUserSerializer)
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
