from django.urls import path

from .views import HomeView, LogoutUser, RegisterUser, StripeConfigView, CreateCheckoutSession, SuccessView, CancelledView, stripe_webhook

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("logout/", LogoutUser.as_view(), name="logout"),
    path("register/", RegisterUser.as_view(), name="register"),
    path("config/", StripeConfigView.as_view(), name="stripe_config"),
    path('create-checkout-session/', CreateCheckoutSession.as_view(), name = "create_checkout_session"), 
    path('success/', SuccessView.as_view()), 
    path('cancelled/', CancelledView.as_view()),
    path('webhook', stripe_webhook, name = 'stripe_webhook'), 
]
