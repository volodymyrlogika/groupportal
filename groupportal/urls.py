from django.contrib import admin
from django.urls import path, include

from django.views.generic import RedirectView
from django.conf.urls.static import static

from . import settings
from accounts.views import CustomLoginView, CustomLogoutView, RegisterView

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('calendar/', include('calendary.urls')),
    path('journal/', include('journal.urls')),

    path('', include('portfolio.urls')),
    path('voting/', include('voting.urls')),
    path('polls/', include('poll.urls')),
    path('forum/', include('forum.urls')),
    path('', include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)