from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from django.http import (
    Http404,
    HttpResponseBadRequest,
    HttpResponseForbidden,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import (
    PortfolioForm,
    PortfolioProjectForm,
    ProjectImageForm,
)
from .models import (
    Portfolio,
    PortfolioProject,
    ProjectImage,
    ProjectVote,
)


# =========================================================
# PORTFOLIO
# =========================================================

@login_required
def portfolio_detail(request):
    """
    Display the current user's private portfolio.

    If the user doesn't have a Portfolio yet (e.g. a brand new
    user who has never visited the edit page), one is created
    automatically instead of returning a 404.
    """
    portfolio, created = Portfolio.objects.get_or_create(
        user=request.user
    )

    portfolio = (
        Portfolio.objects.prefetch_related(
            "projects",
            "projects__images",
        )
        .get(pk=portfolio.pk)
    )

    projects = portfolio.projects.all()

    return render(
        request,
        "portfolio/portfolio_detail.html",
        {
            "portfolio": portfolio,
            "projects": projects,
            "is_owner": True,
        },
    )


@login_required
def portfolio_edit(request):
    """
    Create or edit the current user's portfolio.
    """
    portfolio, created = Portfolio.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        form = PortfolioForm(
            request.POST,
            request.FILES,
            instance=portfolio,
        )

        if form.is_valid():
            form.save()
            return redirect("portfolio_detail")

    else:
        form = PortfolioForm(
            instance=portfolio
        )

    return render(
        request,
        "portfolio/portfolio_form.html",
        {
            "form": form,
            "portfolio": portfolio,
        },
    )


def author_portfolio(request, user_id):
    """
    Display a user's public portfolio and all public projects.
    """
    portfolio = get_object_or_404(
        Portfolio.objects.select_related(
            "user",
        ).prefetch_related(
            "projects__images",
        ),
        user_id=user_id,
    )

    projects = portfolio.projects.filter(
        visibility=PortfolioProject.Visibility.PUBLIC,
    )

    return render(
        request,
        "portfolio/author_portfolio.html",
        {
            "portfolio": portfolio,
            "projects": projects,
            "author": portfolio.user,
        },
    )


# =========================================================
# PROJECTS (private dashboard — owner only)
# =========================================================

@login_required
def project_create(request):
    """
    Create a new project in the current user's portfolio.
    """
    portfolio, created = Portfolio.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        form = PortfolioProjectForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            project = form.save(commit=False)
            project.portfolio = portfolio
            project.save()

            return redirect(
                "project_detail",
                pk=project.pk,
            )

    else:
        form = PortfolioProjectForm()

    return render(
        request,
        "portfolio/project_form.html",
        {
            "form": form,
            "portfolio": portfolio,
        },
    )


@login_required
def project_detail(request, pk):
    """
    Display a project belonging to the current user's portfolio.
    """
    project = get_object_or_404(
        PortfolioProject.objects.select_related(
            "portfolio",
        ).prefetch_related(
            "images",
        ),
        pk=pk,
        portfolio__user=request.user,
    )

    return render(
        request,
        "portfolio/project_detail.html",
        {
            "project": project,
        },
    )


@login_required
def project_edit(request, pk):
    """
    Edit a project belonging to the current user's portfolio.
    """
    project = get_object_or_404(
        PortfolioProject,
        pk=pk,
        portfolio__user=request.user,
    )

    if request.method == "POST":
        form = PortfolioProjectForm(
            request.POST,
            request.FILES,
            instance=project,
        )

        if form.is_valid():
            form.save()

            return redirect(
                "project_detail",
                pk=project.pk,
            )

    else:
        form = PortfolioProjectForm(
            instance=project,
        )

    return render(
        request,
        "portfolio/project_form.html",
        {
            "form": form,
            "project": project,
        },
    )


@login_required
def project_delete(request, pk):
    """
    Delete a project belonging to the current user's portfolio.
    """
    project = get_object_or_404(
        PortfolioProject,
        pk=pk,
        portfolio__user=request.user,
    )

    if request.method == "POST":
        project.delete()
        return redirect("portfolio_detail")

    return render(
        request,
        "portfolio/project_confirm_delete.html",
        {
            "project": project,
        },
    )


# =========================================================
# PROJECT IMAGES
# =========================================================

@login_required
def project_image_add(request, project_pk):
    """
    Add an image to a project belonging to the current user.
    """
    project = get_object_or_404(
        PortfolioProject.objects.select_related(
            "portfolio",
        ),
        pk=project_pk,
        portfolio__user=request.user,
    )

    if request.method == "POST":
        form = ProjectImageForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            image = form.save(commit=False)
            image.project = project
            image.save()

            return redirect(
                "project_detail",
                pk=project.pk,
            )

    else:
        form = ProjectImageForm()

    return render(
        request,
        "portfolio/project_image_form.html",
        {
            "form": form,
            "project": project,
        },
    )


@login_required
def project_image_delete(request, pk):
    """
    Delete an image belonging to the current user's project.
    """
    image = get_object_or_404(
        ProjectImage.objects.select_related(
            "project",
            "project__portfolio",
        ),
        pk=pk,
        project__portfolio__user=request.user,
    )

    project_pk = image.project.pk

    if request.method == "POST":
        image.delete()

        return redirect(
            "project_detail",
            pk=project_pk,
        )

    return render(
        request,
        "portfolio/project_image_confirm_delete.html",
        {
            "image": image,
        },
    )


# =========================================================
# PUBLIC PROJECTS FEED
# =========================================================

@login_required
def public_project_list(request):
    """
    Display all public projects across the whole platform,
    sorted by popularity (likes first).
    """
    projects = PortfolioProject.objects.filter(
        visibility=PortfolioProject.Visibility.PUBLIC,
    ).select_related(
        "portfolio",
        "portfolio__user",
    ).prefetch_related(
        "images",
    ).order_by(
        "-likes_count",
        "-created_at",
    )

    return render(
        request,
        "portfolio/public_project_list.html",
        {
            "projects": projects,
        },
    )


@login_required
def public_project_detail(request, pk):
    """
    Display a single public project.

    Accessible to any logged-in user.
    The owner can also preview their own private project.
    """
    project = get_object_or_404(
        PortfolioProject.objects.select_related(
            "portfolio",
            "portfolio__user",
        ).prefetch_related(
            "images",
        ),
        pk=pk,
    )

    is_owner = project.portfolio.user == request.user

    if not project.is_public and not is_owner:
        raise Http404("Project not found")

    user_vote = None

    if request.user.is_authenticated:
        user_vote = ProjectVote.objects.filter(
            project=project,
            user=request.user,
        ).values_list(
            "value",
            flat=True,
        ).first()

    return render(
        request,
        "portfolio/public_project_detail.html",
        {
            "project": project,
            "is_owner": is_owner,
            "user_vote": user_vote,
        },
    )


# =========================================================
# PROJECT VOTING
# =========================================================

@login_required
@require_POST
def project_vote(request, pk, value):
    """
    Like/dislike a public project.

    value:
        1  = like
        -1 = dislike

    Voting with the same value again removes the vote.
    Voting with the opposite value switches the vote.

    Authors cannot vote on their own projects.
    """
    if value not in (
        ProjectVote.VoteType.LIKE,
        ProjectVote.VoteType.DISLIKE,
    ):
        return HttpResponseBadRequest("Invalid vote value")

    project = get_object_or_404(
        PortfolioProject,
        pk=pk,
        visibility=PortfolioProject.Visibility.PUBLIC,
    )

    if project.portfolio.user == request.user:
        return HttpResponseForbidden(
            "You can't vote on your own project"
        )

    with transaction.atomic():
        project_locked = (
            PortfolioProject.objects
            .select_for_update()
            .get(pk=project.pk)
        )

        existing_vote = ProjectVote.objects.filter(
            project=project_locked,
            user=request.user,
        ).first()

        if existing_vote is None:
            ProjectVote.objects.create(
                project=project_locked,
                user=request.user,
                value=value,
            )

            _apply_vote_delta(
                project_locked,
                value,
                +1,
            )

        elif existing_vote.value == value:
            existing_vote.delete()

            _apply_vote_delta(
                project_locked,
                value,
                -1,
            )

        else:
            _apply_vote_delta(
                project_locked,
                existing_vote.value,
                -1,
            )

            _apply_vote_delta(
                project_locked,
                value,
                +1,
            )

            existing_vote.value = value
            existing_vote.save(
                update_fields=["value"]
            )

    next_url = request.POST.get("next")

    if next_url:
        return redirect(next_url)

    return redirect(
        "public_project_detail",
        pk=project.pk,
    )


# =========================================================
# VOTE COUNTERS
# =========================================================

def _apply_vote_delta(project, vote_value, delta):
    """
    Adjust the denormalized like/dislike counters on a project.

    delta:
        +1 = add vote
        -1 = remove vote
    """
    field = (
        "likes_count"
        if vote_value == ProjectVote.VoteType.LIKE
        else "dislikes_count"
    )

    PortfolioProject.objects.filter(
        pk=project.pk,
    ).update(
        **{
            field: F(field) + delta,
        },
    )

    project.refresh_from_db(
        fields=[field],
    )