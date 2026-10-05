from django.urls import path
from . import views


urlpatterns = [
    path(
        '',
        views.index,
        name='index'
    ),

    path(
        'new',
        views.new
    ),

    path(
        'cart/<int:product_id>',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'cart/remove/<int:product_id>',
        views.remove_from_cart,
        name='remove_from_cart'
    ),

    path(
        'cart/increase/<int:product_id>',
        views.increase_quantity,
        name='increase_quantity'
    ),

    path(
        'cart/decrease/<int:product_id>',
        views.decrease_quantity,
        name='decrease_quantity'
    ),

    path(
        'cart',
        views.cart,
        name='cart'
    ),

    path(
        'checkout',
        views.checkout,
        name='checkout'
    ),

    path(
        'place-order',
        views.place_order,
        name='place_order'
    ),

    path(
        'my-orders',
        views.my_orders,
        name='my_orders'
    ),

    path(
        'my-orders/<int:order_id>',
        views.order_detail,
        name='order_detail'
    ),
]