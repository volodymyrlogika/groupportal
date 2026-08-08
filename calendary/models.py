from django.db import models

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True, null=True)
    meeting_link = models.URLField(blank=True, null=True)
    guest_list = models.ManyToManyField('auth.User', blank=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='events')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
