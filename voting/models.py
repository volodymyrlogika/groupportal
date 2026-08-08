from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
class Poll(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Назва опитування"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Опис"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Автор (Адмін/Модератор)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата створення"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Опитування"
        verbose_name_plural = "Опитування"


class Question(models.Model):
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name="Опитування"
    )
    text = models.CharField(
        max_length=300,
        verbose_name="Текст запитання"
    )
    page = models.PositiveIntegerField(
        default=1,
        verbose_name="Номер сторінки / етап"
    )

    def __str__(self):
        return f"{self.poll.title} — Сторінка {self.page}: {self.text}"

    class Meta:
        verbose_name = "Запитання"
        verbose_name_plural = "Запитання"
        ordering = ["page", "id"]


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices",
        verbose_name="Запитання"
    )
    text = models.CharField(
        max_length=200,
        verbose_name="Варіант відповіді"
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Варіант відповіді"
        verbose_name_plural = "Варіанти відповідей"


class UserAnswer(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Користувач"
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name="Запитання"
    )
    choice = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE,
        verbose_name="Обрана відповідь"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата відповіді"
    )

    def clean(self):
        if self.choice.question_id != self.question_id:
            raise ValidationError(
                "Обраний варіант не належить цьому запитанню."
            )

    def __str__(self):
        return f"{self.user.username} — {self.question.text}"

    class Meta:
        verbose_name = "Відповідь користувача"
        verbose_name_plural = "Відповіді користувачів"
        unique_together = ("user", "question")