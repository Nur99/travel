import logging
from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from auth_.models import MainUser, Activation
from auth_.message import send_html
from utils import messages


logger = logging.getLogger(__name__)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainUser
        fields = ('id', 'full_name', 'avatar', 'birth_date')



class MainUserSerializer(ProfileSerializer):
    class Meta(ProfileSerializer.Meta):
        fields = ProfileSerializer.Meta.fields + ('email', 'timestamp')


class ActivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activation
        fields = ('email', 'full_name', 'created_at', 'end_time')


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=200)
    full_name = serializers.CharField(max_length=300, allow_null=True)

    def complete(self, activation):
        user = MainUser.objects.create_user(self.validated_data['email'],
                                            self.validated_data['password'],
                                            self.validated_data['full_name'])
        activation.is_active = False
        activation.save()
        return user


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    full_name = serializers.CharField(required=False)
    password1 = serializers.CharField(max_length=200)
    password2 = serializers.CharField(max_length=200)

    def validate(self, attrs):
        if Activation.objects.filter(email=attrs['email']).exists():
            logger.warning(messages.USER_EXISTS)
            raise ValidationError(messages.USER_EXISTS)
        if attrs['password1'] != attrs['password2']:
            raise ValidationError(messages.PASSWORD_NOT_SAME)
        return attrs

    def create_activation(self):
        activation = Activation.objects.create(
            email=self.validated_data['email'],
            password=self.validated_data['password1'])
        if self.validated_data.get('full_name'):
            activation.full_name = self.validated_data['full_name']
            activation.save()
        send_html(activation, self.context['request'])
        return activation


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        try:
            user = MainUser.objects.get(email=attrs['email'])
        except MainUser.DoesNotExist:
            raise ValidationError(messages.USER_DOESNOTEXIST)
        if not check_password(attrs['password'], user.password):
            raise ValidationError(messages.USER_DOESNOTEXIST)
        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise ValidationError(messages.PASSWORD_NOT_SAME)
        return attrs

    def change(self):
        user = self.context['user']
        user.set_password(self.validated_data['password1'])
        user.save()
        return user
