from django.urls import path

from .views import PaymentDetailView, PaymentListCreateView

app_name = "pay"


urlpatterns = [
    path("payments/", PaymentListCreateView.as_view(), name="payment-list"),
    path("payments/<int:pk>/", PaymentDetailView.as_view(), name="payment-detail"),
]
