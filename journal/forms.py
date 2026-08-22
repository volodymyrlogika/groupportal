from django import forms
from .models import Grade, Lesson

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'lesson', 'value', 'comment'] # Вкажи свої поля
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'lesson': forms.Select(attrs={'class': 'form-select'}),
            'value': forms.NumberInput(attrs={'class': 'form-control'}),
            'comment': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Фільтрація уроків за викладачем
        if user and not user.is_superuser:
            self.fields['lesson'].queryset = Lesson.objects.filter(subject__teacher=user)