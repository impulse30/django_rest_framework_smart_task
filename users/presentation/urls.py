from django.urls import path
from .views.user_view import ping
from .views.auth_view import register, login

urlpatterns = [
    path("ping/", ping, name="ping"),
    path("register/", register, name="register"),
    path("login/", login, name="login"),
]
