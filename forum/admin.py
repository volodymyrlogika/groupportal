from django.contrib import admin

# Register your models here.

from .models import Topic, Posts, PostImages

admin.site.register(Topic)
admin.site.register(Posts)
admin.site.register(PostImages)