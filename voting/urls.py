from django.urls import path
from . import views

urlpatterns = [
    path('', views.voting_list, name='voting_list'),
    path('<int:pk>/', views.voting_detail, name='voting_detail'),
    path('manage/', views.ManageVotingsView.as_view(), name='manage_voting'),
]