from django import forms
from django.contrib.auth import get_user_model
from .models import Grade, Lesson

User = get_user_model()


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'lesson', 'grade_type', 'value', 'comment']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['student'].queryset = User.objects.filter(
            is_staff=False, 
            is_superuser=False
        )


        if user and not user.is_superuser:
            self.fields['lesson'].queryset = Lesson.objects.filter(
                subject__teacher=user
            ).select_related('subject')