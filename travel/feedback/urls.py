from .views import FeedbackViewSet
from rest_framework.routers import DefaultRouter

app_name = 'feedback'

router = DefaultRouter()
router.register(r'feedback', FeedbackViewSet, base_name='feedback')
# router.register(r'city', CityViewSet, base_name='city')
# router.register(r'country', CountryViewSet, base_name='country')
urlpatterns = router.urls
