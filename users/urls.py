from django.urls import path
from .views import LoginView, SingInView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signin/', SingInView.as_view(), name='signin'),
]