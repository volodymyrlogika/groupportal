from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    PortfolioForm,
    PortfolioProjectForm,
    ProjectImageForm,
)
from .models import (
    Portfolio,
    PortfolioProject,
    ProjectImage,
)


# =========================================================
# PORTFOLIO
# =========================================================

@login_required
def portfolio_detail(request):
    """
    Display the current user's portfolio and all projects.
    """
    portfolio = get_object_or_404(
        Portfolio.objects.prefetch_related(
            "projects",
            "projects__images",
        ),
        user=request.user,
    )

    projects = portfolio.projects.all()

    return render(
        request,
        "portfolio/portfolio_detail.html",
        {
            "portfolio": portfolio,
            "projects": projects,
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


# =========================================================
# PROJECTS
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