from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Cart, CartItem, Customer
from .serializers import CartItemSerializer, CartSerializer, CustomerSerializer


class CustomerListCreateView(generics.ListCreateAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Customer.objects.all().order_by("full_name")
        search = self.request.query_params.get("search")

        if search:
            queryset = queryset.filter(full_name__icontains=search.strip())

        return queryset


class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]


class CartListCreateView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = (
            Cart.objects.select_related("customer", "restaurant")
            .prefetch_related("items__dish")
            .order_by("-updated_at")
        )
        customer_id = self.request.query_params.get("customer")
        restaurant_id = self.request.query_params.get("restaurant")

        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)
        if restaurant_id:
            queryset = queryset.filter(restaurant_id=restaurant_id)

        return queryset


class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.select_related("customer", "restaurant").prefetch_related(
        "items__dish"
    )
    serializer_class = CartSerializer
    permission_classes = [AllowAny]


class CartItemListCreateView(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = CartItem.objects.select_related("cart", "dish", "cart__customer").order_by(
            "id"
        )
        cart_id = self.request.query_params.get("cart")
        dish_id = self.request.query_params.get("dish")

        if cart_id:
            queryset = queryset.filter(cart_id=cart_id)
        if dish_id:
            queryset = queryset.filter(dish_id=dish_id)

        return queryset


class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.select_related("cart", "dish", "cart__customer")
    serializer_class = CartItemSerializer
    permission_classes = [AllowAny]
