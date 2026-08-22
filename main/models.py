from django.conf import settings
from django.db import models


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

    class Visibility(models.TextChoices):
        PRIVATE = "private", "Private"
        PUBLIC = "public", "Public"

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

    visibility = models.CharField(
        max_length=10,
        choices=Visibility.choices,
        default=Visibility.PRIVATE,
        db_index=True
    )

    # Denormalized vote counts, updated on every vote so the
    # public feed can sort without aggregating ProjectVote each time.
    likes_count = models.PositiveIntegerField(
        default=0
    )
    dislikes_count = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["visibility", "-likes_count"]),
        ]

    def __str__(self):
        return self.title

    @property
    def is_public(self):
        return self.visibility == self.Visibility.PUBLIC

    @property
    def rating(self):
        return self.likes_count - self.dislikes_count


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


class ProjectVote(models.Model):

    class VoteType(models.IntegerChoices):
        DISLIKE = -1, "Dislike"
        LIKE = 1, "Like"

    project = models.ForeignKey(
        PortfolioProject,
        on_delete=models.CASCADE,
        related_name="votes"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="project_votes"
    )
    value = models.SmallIntegerField(
        choices=VoteType.choices
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project", "user"],
                name="unique_vote_per_user_per_project"
            )
        ]

    def __str__(self):
        return f"{self.user.username} -> {self.project.title}: {self.get_value_display()}"