import calendar
from datetime import date
from django.utils import timezone

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
from .forms import EventForm



class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        user = self.request.user

        return (
            user.is_superuser
            or user.groups.filter(
                name__in=['Адміністратори', 'Модератори']
            ).exists()
        )


class CalendarView(LoginRequiredMixin, ListView):

    model = Event

    template_name = 'calendary/calendar.html'

    context_object_name = 'events'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        today = date.today()

        # Отримуємо рік і місяць з URL

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


        # Перевірка місяця

        if month < 1:

            month = 12
            year -= 1

        elif month > 12:

            month = 1
            year += 1


        cal = calendar.Calendar(
            firstweekday=0
        )

        weeks = []


        # Події поточного місяця

        events = Event.objects.filter(

            start_time__year=year,

            start_time__month=month

        ).order_by('start_time')


        # Формуємо календар

        for week in cal.monthdatescalendar(
            year,
            month
        ):

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


        # Назви місяців

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


        # Місяці для випадаючого меню

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


        # Роки

        context['years'] = range(

            today.year - 5,

            today.year + 6

        )


        # Попередній місяць

        if month == 1:

            previous_month = 12
            previous_year = year - 1

        else:

            previous_month = month - 1
            previous_year = year


        # Наступний місяць

        if month == 12:

            next_month = 1
            next_year = year + 1

        else:

            next_month = month + 1
            next_year = year


        # Передаємо дані в шаблон

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

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        event = self.object
        now = timezone.now()

        if event.end_time < now:

            status = 'finished'
            status_text = 'Завершено'
            status_class = 'secondary'

        elif event.start_time <= now <= event.end_time:

            status = 'active'
            status_text = 'Зараз проходить'
            status_class = 'success'

        else:

            status = 'planned'
            status_text = 'Заплановано'
            status_class = 'primary'

        context['event_status'] = status
        context['event_status_text'] = status_text
        context['event_status_class'] = status_class

        context['guest_count'] = event.guest_list.count()

        return context




class EventCreateView(StaffRequiredMixin, CreateView):

    model = Event

    form_class = EventForm

    template_name = 'calendary/event_form.html'

    success_url = reverse_lazy('calendar')


    def form_valid(self, form):

        form.instance.author = self.request.user

        return super().form_valid(form)


class EventUpdateView(StaffRequiredMixin, UpdateView):

    model = Event

    form_class = EventForm

    template_name = 'calendary/event_form.html'

    success_url = reverse_lazy('calendar')


class EventDeleteView(StaffRequiredMixin, DeleteView):

    model = Event

    template_name = 'calendary/event_confirm_delete.html'

    success_url = reverse_lazy('calendar')