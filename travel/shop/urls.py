from .views import OrderViewSet, TicketViewSet
from rest_framework.routers import DefaultRouter

app_name = 'shop'

router = DefaultRouter()
router.register(r'order', OrderViewSet, base_name='order')
router.register('ticket', TicketViewSet, base_name='ticket')
urlpatterns = router.urls
