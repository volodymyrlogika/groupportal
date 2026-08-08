from django.contrib import admin

# Register your models here.
from .models import Portfolio, PortfolioProject, ProjectImage

admin.site.register(Portfolio)
admin.site.register(PortfolioProject)
admin.site.register(ProjectImage)
