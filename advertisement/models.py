from django.db import models
from django.conf import settings

class Announcement(models.Model):
    title = models.CharField(
        max_length=255, 
        verbose_name="Заголовок"
    )
    content = models.TextField(
        verbose_name="Текст оголошення"

    )
    image = models.ImageField(
        upload_to='announcements/',
        verbose_name="Зображення",
        null=True,
        blank=True
    )


    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='announcements',
        verbose_name="Автор (Адмін/Модератор)"
    )
    is_important = models.BooleanField(
        default=False, 
        verbose_name="Закріпити нагорі"
    )
    is_active = models.BooleanField(
        default=True, 
        verbose_name="Відображати на сайті"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Дата створення"
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name="Дата оновлення"
    )

    class Meta:
        verbose_name = "Оголошення"
        verbose_name_plural = "Оголошення"
        ordering = ['-is_important', '-created_at']

    def __str__(self):
        return self.title
