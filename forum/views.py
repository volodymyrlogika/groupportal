from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from .models import Posts, Topic


def topic_list(request):
    topics = Topic.objects.order_by('-created_at')
    return render(request, 'forum/topic_list.html', {'topics': topics})










@login_required(login_url='login')
def topic_chat(request, topic_id):
    topic = Topic.objects.get(id=topic_id)

    if not topic:
        messages.error(request, 'Тема не знайдена.')
        return redirect('topic_list')

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        image = request.FILES.get('image')

        if content or image:
            Posts.objects.create(
                topic=topic,
                content=content,
                author=request.user,
                image=image,
            )
            messages.success(request, 'Повідомлення успішно додано.')
            return redirect('topic_chat')

    posts = topic.posts.select_related('author').order_by('created_at')

    return render(request, 'forum/topic_chat.html', {
        'topic': topic,
        'posts': posts,
    })

