from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404

from .forms import PostForm, TopicForm
from .models import Posts, Topic


def topic_list(request):
    topics = Topic.objects.order_by('-created_at')
    return render(request, 'forum/topic_list.html', {'topics': topics})


@login_required(login_url='login')
def create_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST, request.FILES)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.save()
            messages.success(request, 'Тему успішно створено.')
            return redirect('topic_chat', topic_id=topic.id)
    else:
        form = TopicForm()

    return render(request, 'forum/create_topic.html', {'form': form})










@login_required(login_url='login')
def topic_chat(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    reply_text = ''

    if request.method == 'GET':
        reply_post_id = request.GET.get('reply_to')
        if reply_post_id:
            reply_post = topic.posts.filter(id=reply_post_id).select_related('author').first()
            if reply_post:
                reply_text = f'@{reply_post.author.username} '

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
            return redirect('topic_chat', topic_id=topic.id)

    posts = topic.posts.select_related('author').order_by('created_at')

    return render(request, 'forum/topic_chat.html', {
        'topic': topic,
        'posts': posts,
        'reply_text': reply_text,
    })


@login_required(login_url='login')
def toggle_like(request, post_id):
    post = get_object_or_404(Posts, id=post_id)

    if request.method == 'POST':
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

    return redirect('topic_chat', topic_id=post.topic_id)


@login_required(login_url='login')
def edit_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id, author=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пост успішно відредаговано.')
            return redirect('topic_chat', topic_id=post.topic_id)
    else:
        form = PostForm(instance=post)

    return render(request, 'forum/edit_post.html', {
        'form': form,
        'post': post,
    })


@login_required(login_url='login')
def delete_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id, author=request.user)

    if request.method == 'POST':
        topic_id = post.topic_id
        post.delete()
        messages.success(request, 'Пост успішно видалено.')
        return redirect('topic_chat', topic_id=topic_id)

    return redirect('topic_chat', topic_id=post.topic_id)

