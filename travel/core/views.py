from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import PlaceSerializer, PlaceSearchSerializer
from .models import Place, Country, City, PlaceType, PlaceService
from utils.decorators import response_wrapper


@method_decorator(response_wrapper(), name='dispatch')
class PlaceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Place.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PlaceSerializer

    def get_serializer_class(self):
        if self.action == 'search':
            return PlaceSearchSerializer
        return self.serializer_class

    def get_queryset(self):
        queryset = self.queryset
        city = self.request.query_params.get('city')
        if city:
            queryset = queryset.filter(city=City.objects.get(id=city))
        country = self.request.query_params.get('country')
        if country:
            queryset = queryset.filter(city__country=Country.objects.get(id=country))
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
        print(1)
        serializer = self.get_serializer(data=request.data)
        print(2)
        serializer.is_valid(raise_exception=True)
        print(3)
        result = serializer.search(query=query)
        print("result:", result)
        return Response(result)
