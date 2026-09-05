from django.urls import path

from .views import (
    CalendarView,
    EventDetailView,
    EventCreateView,
    EventUpdateView,
    EventDeleteView,    
)


urlpatterns = [

    # Календар
    path(
        '',
        CalendarView.as_view(),
        name='calendar'
    ),

    # Перегляд події
    path(
        'event/<int:pk>/',
        EventDetailView.as_view(),
        name='event_detail'
    ),

    # Створення
    path(
        'event/create/',
        EventCreateView.as_view(),
        name='event_create'
    ),

    # Редагування
    path(
        'event/<int:pk>/edit/',
        EventUpdateView.as_view(),
        name='event_update'
    ),

    # Видалення
    path(
        'event/<int:pk>/delete/',
        EventDeleteView.as_view(),
        name='event_delete'
    ),
]