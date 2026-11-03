from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    RefreshView,
    CurrentUserView
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name = "register"),
    path("login/", LoginView.as_view(), name = "login"),
    path("logout/", LogoutView.as_view(), name = "logout"),
    path("refresh/", RefreshView.as_view(), name = "token-refresh"),
    path("me/", CurrentUserView.as_view(), name = "current-user"),
]