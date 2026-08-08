from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Voting(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Назва голосування"
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
        verbose_name="Автор"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата створення"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Голосування"
        verbose_name_plural = "Голосування"


class VotingOption(models.Model):
    voting = models.ForeignKey(
        Voting,
        on_delete=models.CASCADE,
        related_name="options",
        verbose_name="Голосування"
    )
    text = models.CharField(
        max_length=200,
        verbose_name="Варіант"
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Варіант голосування"
        verbose_name_plural = "Варіанти голосування"


class UserVote(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Користувач"
    )
    voting = models.ForeignKey(
        Voting,
        on_delete=models.CASCADE,
        verbose_name="Голосування"
    )
    option = models.ForeignKey(
        VotingOption,
        on_delete=models.CASCADE,
        verbose_name="Обраний варіант"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата голосування"
    )

    def __str__(self):
        return f"{self.user.username} — {self.voting.title}"

    class Meta:
        verbose_name = "Голос користувача"
        verbose_name_plural = "Голоси користувачів"
        unique_together = ("user", "voting")