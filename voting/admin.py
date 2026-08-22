from django.contrib import admin
from voting.models import UserVote, Voting, VotingOption

# Register your models here.
admin.site.register(Voting)
admin.site.register(VotingOption)
admin.site.register(UserVote)