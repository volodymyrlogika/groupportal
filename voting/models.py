from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Voting(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'голосування'
        verbose_name_plural = 'голосування'

    def __str__(self):
        return self.title


class VotingOption(models.Model):
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=120)

    class Meta:
        verbose_name = 'опція голосування'
        verbose_name_plural = 'опції голосування'

    def __str__(self):
        return self.text


class UserVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE)
    option = models.ForeignKey(VotingOption, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'voting')
        verbose_name = 'голоса користувача'
        verbose_name_plural = 'голоси користувача'

    def __str__(self):
        return f'{self.user.username} - {self.voting.title}'