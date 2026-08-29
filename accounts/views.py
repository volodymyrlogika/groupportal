from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg
from django.utils import timezone

from accounts.forms import LoginForm, RegisterForm
from django.contrib.auth import logout


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    form_class = LoginForm


class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')


class RegisterView(CreateView):
    model = User
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')


def main_page(request):
    """Головна сторінка порталу з інформацією та віджетами-сніпетами всіх розділів."""
    context = {}
    
    # Спроба безпечного імпорту та отримання даних з усіх модулів
    try:
        from calendary.models import Event
        events = Event.objects.order_by('-start_time')[:3]
        events_count = Event.objects.count()
    except Exception:
        events, events_count = [], 0

    try:
        from portfolio.models import PortfolioProject
        projects = PortfolioProject.objects.filter(visibility='public').select_related('portfolio__user').order_by('-likes_count', '-created_at')[:3]
        projects_count = PortfolioProject.objects.count()
    except Exception:
        projects, projects_count = [], 0

    try:
        from forum.models import Topic
        topics = Topic.objects.annotate(posts_count=Count('posts')).select_related('author').order_by('-created_at')[:4]
        topics_count = Topic.objects.count()
    except Exception:
        topics, topics_count = [], 0

    try:
        from voting.models import Voting
        votings = Voting.objects.prefetch_related('options').order_by('-created_at')[:3]
        votings_count = Voting.objects.count()
    except Exception:
        votings, votings_count = [], 0

    try:
        from poll.models import Poll
        polls = Poll.objects.filter(is_active=True).order_by('-created_at')[:3]
        polls_count = Poll.objects.count()
    except Exception:
        polls, polls_count = [], 0

    try:
        from journal.models import Grade, Lesson, Subject
        recent_lessons = Lesson.objects.select_related('subject').order_by('-date')[:3]
        subjects_count = Subject.objects.count()
        
        user_grades = []
        user_avg_grade = None
        if request.user.is_authenticated:
            user_grades = Grade.objects.filter(student=request.user).select_related('lesson__subject', 'grade_type').order_by('-created_at')[:4]
            avg_result = Grade.objects.filter(student=request.user).aggregate(avg=Avg('value'))
            user_avg_grade = avg_result['avg']
    except Exception:
        recent_lessons, subjects_count, user_grades, user_avg_grade = [], 0, [], None

    users_count = User.objects.count()

    context.update({
        'events': events,
        'projects': projects,
        'topics': topics,
        'votings': votings,
        'polls': polls,
        'recent_lessons': recent_lessons,
        'user_grades': user_grades,
        'user_avg_grade': user_avg_grade,
        'stats': {
            'users_count': users_count,
            'projects_count': projects_count,
            'events_count': events_count,
            'topics_count': topics_count,
            'votings_count': votings_count,
            'polls_count': polls_count,
            'subjects_count': subjects_count,
        }
    })

    return render(request, 'index.html', context)