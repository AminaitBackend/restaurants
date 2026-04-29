from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Restaurant API",
        default_version="v1",
        description="API for restaurants, menus, customers, carts, delivery, orders and payments.",
        terms_of_service="https://example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("restaurants.urls")),
    path("api/v1/", include("customer.urls")),
    path("api/v1/", include("delivery.urls")),
    path("api/v1/", include("orders.urls")),
    path("api/v1/", include("pay.urls")),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
