from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Grade, Subject
from .forms import GradeForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

class ModeratorMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.groups.filter(name__in=['Модератори']).exists() and not request.user.is_superuser:
            raise PermissionDenied("Ви не маєте доступу до цієї сторінки.")
        return super().dispatch(request, *args, **kwargs)





# Перегляд оцінок для учня
class StudentJournalView(LoginRequiredMixin, ListView):
    model = Grade
    template_name = 'journal/student_journal.html'
    context_object_name = 'grades'

    def get_queryset(self):
        return Grade.objects.filter(student=self.request.user)

# Перегляд усіх оцінок для вчителя/адміна
class AllGradesListView(ModeratorMixin, ListView):
    model = Grade
    template_name = 'journal/all_grades.html'
    context_object_name = 'grades'

    def get_queryset(self):
        user = self.request.user
        queryset = Grade.objects.select_related('student', 'lesson', 'lesson__subject')
        
        if not user.is_superuser:
            queryset = queryset.filter(lesson__subject__teacher=user)
            
        subject_id = self.request.GET.get('subject')
        if subject_id:
            queryset = queryset.filter(lesson__subject_id=subject_id)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_superuser:
            context['subjects'] = Subject.objects.all()
        else:
            context['subjects'] = Subject.objects.filter(teacher=user)
        context['selected_subject'] = self.request.GET.get('subject', '')
        return context

# Створення оцінки (потрібен для urls.py)
class GradeCreateView(ModeratorMixin, CreateView):
    model = Grade
    form_class = GradeForm
    template_name = 'journal/grade_form.html'
    success_url = reverse_lazy('journal:all_grades')

# Редагування оцінки
class GradeUpdateView(ModeratorMixin, UpdateView):
    model = Grade
    form_class = GradeForm
    template_name = 'journal/grade_form.html'
    success_url = reverse_lazy('journal:all_grades')

# Видалення оцінки
class GradeDeleteView(LoginRequiredMixin, DeleteView):
    model = Grade
    template_name = 'journal/grade_confirm_delete.html'
    success_url = reverse_lazy('journal:all_grades')

