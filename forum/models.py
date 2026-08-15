from django.db import models

# Create your models here.

class Topic(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='topic_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Теми'

class Posts(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(blank=True, null=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_photos/', blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField('auth.User', related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Пости'


class PostImages(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='post_photos/', blank=True, null=True)

    class Meta:
        verbose_name = 'Фото поста'
        verbose_name_plural = 'Фотографії постів'