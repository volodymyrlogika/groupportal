from django import forms

from .models import (
    Portfolio,
    PortfolioProject,
    ProjectImage,
)


class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = [
            "title",
            "description",
            "avatar",
            "github_url",
            "linkedin_url",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter portfolio title",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Tell something about yourself...",
                    "rows": 5,
                }
            ),
            "avatar": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),
            "github_url": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://github.com/username",
                }
            ),
            "linkedin_url": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://linkedin.com/in/username",
                }
            ),
        }


class PortfolioProjectForm(forms.ModelForm):
    class Meta:
        model = PortfolioProject
        fields = [
            "title",
            "description",
            "project_file",
            "project_url",
            "github_url",
            "technologies",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter project title",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Describe your project...",
                    "rows": 6,
                }
            ),
            "project_file": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "project_url": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://example.com",
                }
            ),
            "github_url": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://github.com/username/project",
                }
            ),
            "technologies": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Python, Django, HTML, CSS",
                }
            ),
        }


class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = [
            "image",
        ]

        widgets = {
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),
        }