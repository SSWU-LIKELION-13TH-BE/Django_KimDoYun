from django.urls import path
from .views import post_list, create_post, post_detail, add_reply


urlpatterns = [

    path('', post_list, name='post_list'),
    path('post/new/', create_post, name='create_post'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post/<int:pk>/reply/<int:comment_id>/', add_reply, name='add_reply'),

]