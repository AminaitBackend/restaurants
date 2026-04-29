# Restaurant API

This project contains a Django REST API for restaurants, menu items, customers, carts, delivery addresses, orders, and payments.

## Main apps

- `restaurants`: restaurant categories, owners, restaurants, dish categories, dishes
- `customer`: customers, carts, cart items
- `delivery`: delivery addresses
- `orders`: orders, order items
- `pay`: payments

## API base URL

- `/api/v1/`

## Main endpoints

- `/api/v1/restaurants/`
- `/api/v1/restaurant-categories/`
- `/api/v1/restaurant-owners/`
- `/api/v1/dish-categories/`
- `/api/v1/dishes/`
- `/api/v1/customers/`
- `/api/v1/carts/`
- `/api/v1/cart-items/`
- `/api/v1/delivery-addresses/`
- `/api/v1/orders/`
- `/api/v1/order-items/`
- `/api/v1/payments/`

Each endpoint supports list/create on the collection URL and retrieve/update/delete on `/<id>/`.

## API documentation

- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`

## Notes

- Dishes can be filtered by query parameters:
  - `/api/v1/dishes/?restaurant=1`
  - `/api/v1/dishes/?category=2`
- The project uses Django REST Framework and `drf_yasg` for schema generation.
