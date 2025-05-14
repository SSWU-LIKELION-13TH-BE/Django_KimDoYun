from django.urls import path
from .views import signup_view, login_view, home, logout_view, mypage, edit_profile, guestbook_list, guestbook_write, user_list
from django.contrib.auth import views as auth_views
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('home/', home, name='home'),
    path('logout/', logout_view, name='logout'),
    path('mypage/', mypage, name='mypage'),
    path('mypage/edit/', edit_profile, name='edit_profile'),
    path('<str:username>/guestbook/', guestbook_list, name='guestbook_list'),
    path('<str:username>/guestbook/write/', guestbook_write, name='guestbook_write'),
    path('users/', user_list, name='user_list'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),  

]