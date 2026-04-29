from .views import CartView,CartItemCreateView,CartItemUpdateView,CartItemDeleteView,CartClearview
from django.urls import path
urlpatterns = [
    path('cart/', CartView.as_view()),
    path('cart/items/', CartItemCreateView.as_view()),
    path('cart/items/<int:pk>/', CartItemUpdateView.as_view()),
    path('cart/items/<int:id>/', CartItemDeleteView.as_view()),
    path('cart/clear/', CartClearview.as_view()),
]