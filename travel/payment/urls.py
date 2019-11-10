from . import views
from django.urls import path
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('card_detail/<int:id>/', views.CardDetail.as_view())
]

router = DefaultRouter()
router.register(r'payment', views.PaymentViewSet, base_name='payment')
urlpatterns += router.urls
