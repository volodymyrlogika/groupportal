from django.urls import path
from . import views

urlpatterns = [
    path("", views.PollListView.as_view(), name="poll_list"),
    path("<int:pk>/", views.PollDetailView.as_view(), name="poll_detail"),
    path("<int:pk>/start/", views.PollStartView.as_view(), name="poll_start"),
    path("<int:pk>/result/", views.PollResultView.as_view(), name="poll_result"),
    path("create/",views.PollQuestionView.as_view(),name="poll_question"),
]