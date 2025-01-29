from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("cart/", views.view_cart, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path(
        "cart/remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"
    ),
    path("checkout/", views.checkout, name="checkout"),
    path("<slug:slug>/", views.product_detail, name="product_detail"),
    path("order/<int:orderId>/", views.order_detail, name="order_detail"),
]
