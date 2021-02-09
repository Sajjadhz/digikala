from django.urls import path

from .views import login_view, RegisterView, register_view, logout_view, LogoutView

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
]
