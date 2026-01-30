from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.posts_view, name='posts'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('dislike_post/<int:post_id>/', views.dislike_post, name='dislike_post'),
]