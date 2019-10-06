from django.urls import path
from rest_framework.routers import DefaultRouter

from auth_.views import ActivationViewSet

urlpatterns = [
]

router = DefaultRouter()
router.register(r'activations', ActivationViewSet, base_name='activation')
urlpatterns += router.urls
