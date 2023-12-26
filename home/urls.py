from django.urls import path
from . import views

urlpatterns = [
    path('', views.hotel, name="hotel"),
    path('login/', views.login_page, name="login"),
    path('register/', views.register_page, name="register")
]
