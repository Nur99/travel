from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import (AddRatingSerializer, PlaceSerializer,
                          PlaceSearchSerializer, CitySerializer,
                          CountrySerializer)
from .models import Place, Country, City
from utils.decorators import response_wrapper


@method_decorator(response_wrapper(), name='dispatch')
class PlaceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Place.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PlaceSerializer

    def get_serializer_class(self):
        if self.action == 'search':
            return PlaceSearchSerializer
        if self.action == 'add_rating':
            return AddRatingSerializer
        return self.serializer_class

    def get_queryset(self):
        queryset = self.queryset
        city = self.request.query_params.get('city')
        if city:
            queryset = queryset.filter(city_id=city)
        country = self.request.query_params.get('country')
        if country:
            queryset = queryset.filter(city__country=country)
        price_min = self.request.query_params.get('price_min')
        price_max = self.request.query_params.get('price_max')
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)
        return queryset

    @action(methods=['post'], detail=False)
    def search(self, request):
        query = request.data['query']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.search(query=query)
        return Response(result)

    @action(permission_classes=[IsAuthenticated, ],
            methods=['post'], detail=True)
    def add_rating(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.add_rating(place=instance, user=request.user)
        return Response(result)


@method_decorator(response_wrapper(), name='dispatch')
class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CitySerializer

    def get_queryset(self):
        country_id = self.request.query_params.get('country_id')
        return City.objects.filter(country_id=country_id)


@method_decorator(response_wrapper(), name='dispatch')
class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CountrySerializer
