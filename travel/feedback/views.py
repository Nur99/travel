from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import FeedbackSerializer
from .models import Feedback
from utils.decorators import response_wrapper


@method_decorator(response_wrapper(), name='dispatch')
class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.filter(is_active=True)
    permission_classes = (IsAuthenticated, )
    serializer_class = FeedbackSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
