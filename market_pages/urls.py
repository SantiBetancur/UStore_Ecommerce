from django.urls import path
from .views import LandingView
from .views.CartView import view_cart, add_to_cart, remove_from_cart, clear_cart
from .views import CartView

urlpatterns = [
    path('', LandingView.as_view(), name='landing'),
    path("cart/", CartView.view_cart, name="view_cart"),
    path("cart/add/<int:product_id>/", CartView.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", CartView.remove_from_cart, name="remove_from_cart"),
    path("cart/clear/", CartView.clear_cart, name="clear_cart"),
]

