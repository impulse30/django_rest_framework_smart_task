from django.urls import path
from .views.user_view import ping
from .views.auth_view import RegisterView, LoginView

urlpatterns = [
    path("ping/", ping, name="ping"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
]
