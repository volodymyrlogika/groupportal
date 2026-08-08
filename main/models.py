from django.db import models
from django.conf import settings


class Portfolio(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="portfolio"
    )
    title = models.CharField(
        max_length=200,
        blank=True
    )
    description = models.TextField(
        blank=True
    )
    avatar = models.ImageField(
        upload_to="portfolio/avatars/",
        blank=True,
        null=True
    )
    github_url = models.URLField(
        blank=True
    )
    linkedin_url = models.URLField(
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Portfolio of {self.user.username}"


class PortfolioProject(models.Model):
    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name="projects"
    )
    title = models.CharField(
        max_length=200
    )
    description = models.TextField()

    project_file = models.FileField(
        upload_to="portfolio/projects/files/",
        blank=True,
        null=True
    )

    project_url = models.URLField(
        blank=True
    )
    github_url = models.URLField(
        blank=True
    )

    technologies = models.CharField(
        max_length=500,
        blank=True,
        help_text="Example: Python, Django, HTML, CSS"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(
        PortfolioProject,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(
        upload_to="portfolio/projects/images/"
    )

    def __str__(self):
        return f"Image for {self.project.title}"