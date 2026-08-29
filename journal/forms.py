from django import forms
from django.contrib.auth.models import User
from .models import Grade, Lesson

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'lesson', 'value', 'comment']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'lesson': forms.Select(attrs={'class': 'form-select'}),
            'value': forms.NumberInput(attrs={'class': 'form-control'}),
            'comment': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['student'].queryset = User.objects.filter(is_staff=False, is_superuser=False)


        if user and not user.is_superuser:
            self.fields['lesson'].queryset = Lesson.objects.filter(subject__teacher=user)