import calendar
from datetime import date

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


# =========================
# ГОЛОВНА СТОРІНКА КАЛЕНДАРЯ
# =========================

class CalendarView(LoginRequiredMixin, ListView):

    model = Event
    template_name = 'calendary/calendar.html'
    context_object_name = 'events'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        today = date.today()

        # Отримуємо рік і місяць з адреси
        try:
            year = int(
                self.request.GET.get(
                    'year',
                    today.year
                )
            )

            month = int(
                self.request.GET.get(
                    'month',
                    today.month
                )
            )

        except ValueError:

            year = today.year
            month = today.month


        # Якщо місяць вийшов за межі
        if month < 1:

            month = 12
            year -= 1

        elif month > 12:

            month = 1
            year += 1


        # Календар починається з понеділка
        cal = calendar.Calendar(firstweekday=0)

        weeks = []


        # Події поточного місяця
        events = Event.objects.filter(
            start_time__year=year,
            start_time__month=month
        ).order_by('start_time')


        # Створюємо тижні
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

                    'current_month':
                        day.month == month,

                    'today':
                        day == today,

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


    

        context['month_names'] = [

            (1, 'Січень'),
            (2, 'Лютий'),
            (3, 'Березень'),
            (4, 'Квітень'),
            (5, 'Травень'),
            (6, 'Червень'),
            (7, 'Липень'),
            (8, 'Серпень'),
            (9, 'Вересень'),
            (10, 'Жовтень'),
            (11, 'Листопад'),
            (12, 'Грудень'),

        ]


        context['years'] = range(
            today.year - 5,
            today.year + 6
        )


        if month == 1:

            previous_month = 12
            previous_year = year - 1

        else:

            previous_month = month - 1
            previous_year = year


        if month == 12:

            next_month = 1
            next_year = year + 1

        else:

            next_month = month + 1
            next_year = year



        context['weeks'] = weeks

        context['month_name'] = month_names[month]

        context['year'] = year

        context['current_month'] = month

        context['previous_month'] = previous_month
        context['previous_year'] = previous_year

        context['next_month'] = next_month
        context['next_year'] = next_year


        return context



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


    def form_valid(self, form):

        form.instance.author = self.request.user

        return super().form_valid(form)


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