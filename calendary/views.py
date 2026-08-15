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
import calendar
from datetime import date


# Перевірка прав адміністратора або модератора
class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        user = self.request.user

        return (
            user.is_superuser
            or user.groups.filter(
                name__in=['Адміністратори', 'Модератори']
            ).exists()
        )


# Головна сторінка календаря
class CalendarView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'calendary/calendar.html'
    context_object_name = 'events'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = date.today()

        year = today.year
        month = today.month

        cal = calendar.Calendar(firstweekday=0)

        weeks = []

        events = Event.objects.filter(
            start_time__year=year,
            start_time__month=month
        ).order_by('start_time')

        for week in cal.monthdatescalendar(year, month):

            week_data = []

            for day in week:

                day_events = [
                    event
                    for event in events
                    if event.start_time.date() == day
                ]

                week_data.append({
                    'date': day,
                    'events': day_events,
                    'current_month': day.month == month,
                    'today': day == today,
                })

            weeks.append(week_data)

        month_names = [
            '',
            'Січень',
            'Лютий',
            'Березень',
            'Квітень',
            'Травень',
            'Червень',
            'Липень',
            'Серпень',
            'Вересень',
            'Жовтень',
            'Листопад',
            'Грудень',
        ]

        context['weeks'] = weeks
        context['month_name'] = month_names[month]
        context['year'] = year

        return context


# Перегляд конкретної події
class EventDetailView(LoginRequiredMixin, DetailView):

    model = Event
    template_name = 'calendary/event_detail.html'
    context_object_name = 'event'


# Створення події
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

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# Редагування події
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


# Видалення події
class EventDeleteView(StaffRequiredMixin, DeleteView):

    model = Event
    template_name = 'calendary/event_confirm_delete.html'

    success_url = reverse_lazy('calendar')