from django.urls import path
from .views import (
    StudentJournalView, 
    AllGradesListView, 
    GradeCreateView,
    GradeUpdateView,
    GradeDeleteView
)

app_name = 'journal'

urlpatterns = [
    # 1. Особистий щоденник
    path('my-journal/', StudentJournalView.as_view(), name='student_journal'),
    
    # 2. Перегляд усіх оцінок
    path('grades/', AllGradesListView.as_view(), name='all_grades'),
    
    # 3. Створення оцінки
    path('grades/add/', GradeCreateView.as_view(), name='grade_create'),
    
    # 4. Редагування оцінки
    path('grades/<int:pk>/edit/', GradeUpdateView.as_view(), name='grade_update'),
    
    # 5. Видалення оцінки під питанням
    path('grades/<int:pk>/delete/', GradeDeleteView.as_view(), name='grade_delete'),
]

