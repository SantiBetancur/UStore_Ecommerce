from django.urls import path
from .views.index import LoginView, SingInView
from .views.LogOut import LogOutView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signin/', SingInView.as_view(), name='signin'),
    path('logout/', LogOutView.as_view(), name='logout'),
]