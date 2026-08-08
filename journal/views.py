# journal/views.py

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from .models import Grade, Subject
from django.views.generic import UpdateView, DeleteView

# Перевірте, чи є у вас цей клас:
class StudentJournalView(LoginRequiredMixin, ListView):
    model = Grade
    template_name = 'journal/student_journal.html'
    context_object_name = 'grades'

    def get_queryset(self):
        return Grade.objects.filter(student=self.request.user)\
                            .select_related('lesson', 'lesson__subject', 'grade_type')


class StaffOrModeratorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (
            user.is_staff or 
            user.is_superuser or 
            user.groups.filter(name='Moderators').exists()
        )


class AllGradesListView(StaffOrModeratorRequiredMixin, ListView):
    model = Grade
    template_name = 'journal/all_grades.html'
    context_object_name = 'grades'
    paginate_by = 20

    def get_queryset(self):
        queryset = Grade.objects.select_related('student', 'lesson', 'lesson__subject', 'grade_type')
        subject_id = self.request.GET.get('subject')
        if subject_id:
            queryset = queryset.filter(lesson__subject_id=subject_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subjects'] = Subject.objects.all()
        context['selected_subject'] = self.request.GET.get('subject', '')
        return context



class GradeCreateView(StaffOrModeratorRequiredMixin, CreateView):
    """Створення нової оцінки."""
    model = Grade
    fields = ['student', 'lesson', 'grade_type', 'value', 'comment']
    template_name = 'journal/grade_form.html'
    success_url = reverse_lazy('journal:all_grades')


from django.views.generic import UpdateView, DeleteView


class GradeUpdateView(StaffOrModeratorRequiredMixin, UpdateView):
    """Редагування оцінки."""
    model = Grade
    fields = ['student', 'lesson', 'grade_type', 'value', 'comment']
    template_name = 'journal/grade_form.html' 
    success_url = reverse_lazy('journal:all_grades')


class GradeDeleteView(StaffOrModeratorRequiredMixin, DeleteView):
    """Видалення оцінки."""
    model = Grade
    template_name = 'journal/grade_confirm_delete.html'
    success_url = reverse_lazy('journal:all_grades')