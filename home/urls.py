from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.hotel, name="hotel"),
    path("hotel_details/<uid>/", views.hotel_details, name='hotel_details'),
    path('login/', views.login_page, name="login"),
    path('register/', views.register_page, name="register"),
    path('log_out/', views.log_out, name="log_out")
    
]
