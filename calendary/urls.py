from django.urls import path
from .views import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

urlpatterns = [
    path('', ListView.as_view(), name='calendar'),

    path(
        'event/<int:pk>/',
        DetailView.as_view(),
        name='event_detail'
    ),

    path(
        'event/create/',
        CreateView.as_view(),
        name='event_create'
    ),

    path(
        'event/<int:pk>/edit/',
        UpdateView.as_view(),
        name='event_update'
    ),

    path(
        'event/<int:pk>/delete/',
        DeleteView.as_view(),
        name='event_delete'
    ),
]