from django.urls import path
from .views import (
    StudentJournalView,
    AllGradesListView,
    GradeCreateView,
    GradeUpdateView,
    GradeDeleteView,
)

app_name = 'journal'


urlpatterns = [
    path('my-journal/', StudentJournalView.as_view(), name='student_journal'),
    path('grades/', AllGradesListView.as_view(), name='all_grades'),
    path('grades/add/', GradeCreateView.as_view(), name='grade_create'),
    path('grades/<int:pk>/edit/', GradeUpdateView.as_view(), name='grade_update'),
    path('grades/<int:pk>/delete/', GradeDeleteView.as_view(), name='grade_delete'),
]