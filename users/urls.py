from django.urls import path
from .views.index import LoginView, SingInView
from .views.LogOut import LogOutView
from .views.googleLoginView import google_login_wrapper

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("signin/", SingInView.as_view(), name="signin"),
    path("logout/", LogOutView.as_view(), name="logout"),
    path("google-login/", google_login_wrapper, name="google_login_direct"),
]
