from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Subject(models.Model):
    """Модель навчального предмета (наприклад: Математика, Фізика, Історія)."""
    title = models.CharField(max_length=100, verbose_name="Назва предмета")
    description = models.TextField(blank=True, verbose_name="Опис предмета")
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="taught_subjects",
        verbose_name="Викладач"
    )

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предмети"
        ordering = ['title']

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель конкретного заняття/уроку."""
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Предмет"
    )
    title = models.CharField(max_length=200, verbose_name="Тема уроку")
    date = models.DateField(verbose_name="Дата проведення")
    description = models.TextField(blank=True, verbose_name="Короткий зміст/Опис")
    homework = models.TextField(blank=True, verbose_name="Домашнє завдання")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ['-date']

    def __str__(self):
        return f"{self.subject.title} - {self.title} ({self.date.strftime('%d.%m.%Y')})"


class GradeType(models.Model):
    """Тип оцінки (наприклад: Домашня робота, Контрольна робота, Модуль, Лабораторна)."""
    name = models.CharField(max_length=50, verbose_name="Тип оцінки")
    weight = models.PositiveIntegerField(
        default=1,
        help_text="Вага оцінки для розрахунку середнього балу (за потреби)",
        verbose_name="Вага"
    )

    class Meta:
        verbose_name = "Тип оцінки"
        verbose_name_plural = "Типи оцінок"

    def __str__(self):
        return self.name


class Grade(models.Model):
    """Модель оцінки конкретного студента."""
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="grades",
        verbose_name="Студент/Учень"
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="grades",
        verbose_name="Урок"
    )
    grade_type = models.ForeignKey(
        GradeType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Тип оцінювання"
    )
    # Значення оцінки (наприклад, від 1 до 12)
    value = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name="Оцінка"
    )
    comment = models.CharField(
        max_length=255, 
        blank=True, 
        verbose_name="Коментар викладача"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата виставлення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата редагування")

    class Meta:
        verbose_name = "Оцінка"
        verbose_name_plural = "Оцінки"
        # Один студент може отримати тільки одну оцінку за один конкретний урок
        unique_together = ('student', 'lesson')
        ordering = ['-lesson__date']

    def __str__(self):
        return f"{self.student} — {self.lesson.subject.title}: {self.value}"