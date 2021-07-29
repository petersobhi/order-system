from rest_framework import viewsets, permissions, mixins, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Product, Order
from core.permissions import IsSeller, IsBuyer
from core.serializers import CategorySerializer, ProductSerializer, OrderSerializer, OrderItemSerializer


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser, IsSeller]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    def get_queryset(self):
        currency = self.request.GET.get('currency', 'EGP')
        return Product.objects.with_converted_price(currency)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsBuyer]

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user)


class OrderItemCreateView(generics.CreateAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]


class RevenueAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        revenue = Order.objects.revenue()
        return Response(revenue)
