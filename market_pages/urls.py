from django.urls import path
from .views import LandingView
from .views.CartView import view_cart, add_to_cart, remove_from_cart, clear_cart
from .views import CartView
from .views.SearchView import search_products
from .views import LandingView, CreateStore, AdminStore

urlpatterns = [
    path('', LandingView.as_view(), name='landing'),
    path("cart/", CartView.view_cart, name="view_cart"),
    path("cart/add/<int:product_id>/", CartView.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", CartView.remove_from_cart, name="remove_from_cart"),
    path("cart/clear/", CartView.clear_cart, name="clear_cart"),
    path("search/", search_products, name="search_products"),
    path('create-store/', CreateStore.as_view(), name='create_store'),
    path('admin-store/', AdminStore.as_view(), name='admin_store'),
]

