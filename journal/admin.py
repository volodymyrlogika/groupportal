from django.contrib import admin
from .models import Subject, Lesson, GradeType, Grade

admin.site.register(Subject)
admin.site.register(Lesson)
admin.site.register(GradeType)
admin.site.register(Grade)
