from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Announcement
from .forms import AnnouncementForm


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff


class AnnouncementListView(ListView):
    model = Announcement
    template_name = 'advertisement/announcement_list.html'
    context_object_name = 'announcements'

    def get_queryset(self):
        return Announcement.objects.filter(is_active=True)


class AnnouncementDetailView(DetailView):
    model = Announcement
    template_name = 'advertisement/announcement_detail.html'
    context_object_name = 'announcement'

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return Announcement.objects.all()
        return Announcement.objects.filter(is_active=True)


class AnnouncementCreateView(StaffRequiredMixin, CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'advertisement/announcement_form.html'
    success_url = reverse_lazy('advertisement:list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AnnouncementUpdateView(StaffRequiredMixin, UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'advertisement/announcement_form.html'
    success_url = reverse_lazy('advertisement:list')


class AnnouncementDeleteView(StaffRequiredMixin, DeleteView):
    model = Announcement
    template_name = 'advertisement/announcement_confirm_delete.html'
    success_url = reverse_lazy('advertisement:list')