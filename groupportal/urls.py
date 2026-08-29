from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from accounts.views import CustomLoginView, CustomLogoutView, RegisterView

urlpatterns = [
    
    path('', RedirectView.as_view(url='/login/', permanent=False)),

    path('admin/', admin.site.urls),
    path('journal/', include('journal.urls')),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]