from django.shortcuts import render
from django.views.generic import ListView, DetailView, View

from poll.models import Poll

# Create your views here.
class PollListView(ListView):
    model = Poll
    template_name = "poll/poll_list.html"
    context_object_name = "polls"

class PollDetailView(DetailView):
    model = Poll
    template_name = "poll/poll_detail.html"
    context_object_name = "poll"

class StartPollView(View):
    model = Poll
    template_name = "poll/poll_start.html"
    context_object_name = "poll"

class PollResultView(View):
    model = Poll
    template_name = "poll/poll_result.html"
    context_object_name = "poll"