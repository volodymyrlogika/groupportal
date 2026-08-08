from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Event


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        user = self.request.user

        return (
            user.is_superuser
            or user.groups.filter(
                name__in=['Адміністратори', 'Модератори']
            ).exists()
        )


class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'calendary/event_list.html'
    context_object_name = 'events'
    ordering = ['start_time']


class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'calendary/event_detail.html'
    context_object_name = 'event'


class EventCreateView(StaffRequiredMixin, CreateView):
    model = Event

    template_name = 'calendary/event_form.html'

    fields = [
        'title',
        'description',
        'start_time',
        'end_time',
        'location',
        'meeting_link',
        'guest_list',
    ]

    success_url = reverse_lazy('calendar')


class EventUpdateView(StaffRequiredMixin, UpdateView):
    model = Event

    template_name = 'calendary/event_form.html'

    fields = [
        'title',
        'description',
        'start_time',
        'end_time',
        'location',
        'meeting_link',
        'guest_list',
    ]

    success_url = reverse_lazy('calendar')


class EventDeleteView(StaffRequiredMixin, DeleteView):
    model = Event

    template_name = 'calendary/event_confirm_delete.html'

    success_url = reverse_lazy('calendar')