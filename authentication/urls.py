from django.urls import path

from .views import HomeView, LogoutUser, RegisterUser

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    # path("login/", LoginUser.as_view(), name="login"),
    path("logout/", LogoutUser.as_view(), name="logout"),
    path("register/", RegisterUser.as_view(), name="register"),
]
