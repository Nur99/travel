from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('id', 'user', 'description', )
