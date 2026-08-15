from django.urls import path
from . import views

urlpatterns = [
     path('', views.topic_list, name='topic_list'),
     path('topic_chat/<int:topic_id>/', views.topic_chat, name='topic_chat'),
]
