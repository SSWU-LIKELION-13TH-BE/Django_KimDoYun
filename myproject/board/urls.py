from django.urls import path
from .views import post_list, create_post, post_detail


urlpatterns = [

    path('', post_list, name='post_list'),
    path('post/new/', create_post, name='create_post'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
]