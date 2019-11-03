# from .views import PlaceViewSet, CityViewSet, CountryViewSet
from rest_framework.routers import DefaultRouter
#
app_name = 'shop'
#
router = DefaultRouter()
# router.register(r'place', PlaceViewSet, base_name='place')
# router.register(r'city', CityViewSet, base_name='city')
# router.register(r'country', CountryViewSet, base_name='country')
urlpatterns = router.urls
