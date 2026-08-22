from django.urls import path
from . import views

urlpatterns = [
     path('', views.topic_list, name='topic_list'),
     path('topic/new/', views.create_topic, name='create_topic'),
     path('topic_chat/<int:topic_id>/', views.topic_chat, name='topic_chat'),
     path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
     path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
     path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
]
