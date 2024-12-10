from django.urls import path
from .views import register, profile, seller_profile
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView

app_name = "users"

urlpatterns = [
    path('register/', register, name="register"),
    path('login/', LoginView.as_view(template_name = "users/login.html"), name="login"),
    path('logout/', TemplateView.as_view(template_name = "users/logout.html"), name="logout"),
    path('profile/', profile, name="profile"),
    path('sellerprofile/<int:id>/', seller_profile, name="sellerprofile"),

]