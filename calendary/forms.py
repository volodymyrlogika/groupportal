from django import forms
from django.core.exceptions import ValidationError

from .models import Event


class EventForm(forms.ModelForm):

    class Meta:
        model = Event

        fields = [
            'title',
            'description',
            'start_time',
            'end_time',
            'location',
            'meeting_link',
            'guest_list',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Наприклад: Зустріч групи',
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Опишіть подію...',
                'rows': 5,
            }),

            'start_time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),

            'end_time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),

            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Наприклад: Кабінет 204',
            }),

            'meeting_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://...',
            }),

            'guest_list': forms.SelectMultiple(attrs={
                'class': 'form-select',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:

            if end_time <= start_time:
                raise ValidationError(
                    'Час завершення події повинен бути пізніше часу початку.'
                )

        return cleaned_data