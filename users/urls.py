from django.urls import path
from .views.index import LoginView, SingInView
from .views.LogOut import LogOutView
from allauth.socialaccount.providers.google.views import oauth2_login

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("signin/", SingInView.as_view(), name="signin"),
    path("logout/", LogOutView.as_view(), name="logout"),
    path("google-login/", oauth2_login, name="google_login_direct"),
]
