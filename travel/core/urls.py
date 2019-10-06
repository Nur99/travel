from .views import PlaceViewSet
from rest_framework.routers import DefaultRouter

app_name = 'travel'

router = DefaultRouter()
router.register(r'place', PlaceViewSet, base_name='place')
urlpatterns = router.urls
