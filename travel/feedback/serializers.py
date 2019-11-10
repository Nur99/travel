from rest_framework import serializers

from .models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        read_only_fields = ('user', )
        fields = ('user', 'message', )
        depth = 2
