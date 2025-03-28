from django.urls import path
from .views import signup_view, login_view, home

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('home/', home, name='home'),
]