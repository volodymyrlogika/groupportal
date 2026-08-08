from django.urls import path

from . import views


urlpatterns = [
    # Portfolio
    path(
        "portfolio/",
        views.portfolio_detail,
        name="portfolio_detail",
    ),
    path(
        "portfolio/edit/",
        views.portfolio_edit,
        name="portfolio_edit",
    ),

    # Projects
    path(
        "portfolio/projects/create/",
        views.project_create,
        name="project_create",
    ),
    path(
        "portfolio/projects/<int:pk>/",
        views.project_detail,
        name="project_detail",
    ),
    path(
        "portfolio/projects/<int:pk>/edit/",
        views.project_edit,
        name="project_edit",
    ),
    path(
        "portfolio/projects/<int:pk>/delete/",
        views.project_delete,
        name="project_delete",
    ),

    # Project images
    path(
        "portfolio/projects/<int:project_pk>/images/add/",
        views.project_image_add,
        name="project_image_add",
    ),
    path(
        "portfolio/images/<int:pk>/delete/",
        views.project_image_delete,
        name="project_image_delete",
    ),
]