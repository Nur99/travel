from . import views
from django.urls import path
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('pay/<str:id>/', views.PayTicket.as_view())
]

router = DefaultRouter()
router.register(r'payment', views.PaymentViewSet, base_name='payment')
urlpatterns += router.urls
