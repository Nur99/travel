from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import PlaceSerializer
from .models import Place, Country, City, PlaceType, PlaceService
from utils.decorators import response_wrapper


@method_decorator(response_wrapper(), name='dispatch')
class PlaceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Place.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PlaceSerializer

    def get_queryset(self):
        queryset = Place.objects.all()
        if self.request.query_params.get("city"):
            queryset = queryset.filter(city__name='Almaty')
        return queryset

