from django.urls import path
from .views import LandingView, CreateStore, AdminStore

urlpatterns = [
    path('', LandingView.as_view(), name='landing'),
    path('create-store/', CreateStore.as_view(), name='create_store'),
    path('admin-store/', AdminStore.as_view(), name='admin_store'),
]