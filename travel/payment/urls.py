from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'paybox', views.PayboxViewSet, base_name='paybox')
router.register(r'payment', views.PaymentViewSet, base_name='payment')
urlpatterns = router.urls
