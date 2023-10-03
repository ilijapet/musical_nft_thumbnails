from django.urls import path

from .views import HomeView, LogoutUser

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    # path("login/", LoginUser.as_view(), name="login"),
    path("logout/", LogoutUser.as_view(), name="logout"),
]
