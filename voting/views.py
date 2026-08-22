from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from .models import Voting, VotingOption, UserVote


class ModeratorMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        if not request.user.groups.filter(name__in=['Модератори']).exists() and not request.user.is_superuser:
            raise PermissionDenied("Ви не маєте доступу до цієї сторінки.")

        return super().dispatch(request, *args, **kwargs)


def voting_list(request):
    votings = Voting.objects.all().order_by('-created_at')
    return render(request, 'voting/voting_list.html', {'votings': votings})


@login_required
def voting_detail(request, pk):
    voting = get_object_or_404(Voting, pk=pk)
    options = voting.options.all()

    total_votes = 0
    for option in options:
        option.votes_count = UserVote.objects.filter(option=option).count()
        total_votes += option.votes_count

    for option in options:
        if total_votes > 0:
            option.percent = int((option.votes_count / total_votes) * 100)
        else:
            option.percent = 0

    user_vote = UserVote.objects.filter(user=request.user, voting=voting).first()

    if request.method == 'POST':
        option_id = request.POST.get('option')

        if option_id:
            selected_option = get_object_or_404(VotingOption, pk=option_id, voting=voting)
            UserVote.objects.update_or_create(
                user=request.user,
                voting=voting,
                defaults={'option': selected_option}
            )
            return redirect('voting_detail', pk=voting.pk)

    context = {
        'voting': voting,
        'options': options,
        'user_vote': user_vote,
        'total_votes': total_votes,
    }
    return render(request, 'voting/voting_detail.html', context)


class ManageVotingsView(ModeratorMixin, View):
    def get(self, request):
        votings = Voting.objects.all().order_by('-created_at')

        for voting in votings:
            voting.votes_count = UserVote.objects.filter(voting=voting).count()

        context = {'votings': votings}
        return render(request, 'voting/manage_votings.html', context)

    def post(self, request):
        action = request.POST.get('action')

        if action == 'create':
            title = request.POST.get('title')
            description = request.POST.get('description')
            options = request.POST.getlist('options')

            if not title or not title.strip():
                messages.error(request, 'Введіть назву голосування.')
                return redirect('manage_voting')

            valid_options = []
            for option in options:
                if option.strip():
                    valid_options.append(option.strip())

            if len(valid_options) < 2:
                messages.error(request, 'Додайте щонайменше 2 варіанти.')
                return redirect('manage_voting')

            voting = Voting.objects.create(
                title=title.strip(),
                description=description.strip(),
                created_by=request.user
            )

            for option in valid_options:
                VotingOption.objects.create(voting=voting, text=option)

            messages.success(request, 'Голосування успішно створено.')

        elif action == 'delete':
            voting_id = request.POST.get('voting_id')
            voting = get_object_or_404(Voting, pk=voting_id)
            voting.delete()
            messages.success(request, 'Голосування успішно видалено.')

        return redirect('manage_voting')