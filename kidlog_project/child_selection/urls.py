from django.urls import path
from . import views

urlpatterns = [
    path("add-child/", views.add_child_view, name="add_child"),
    path("", views.child_selection_view, name="child_selection"),
    path(
        "delete_child/<int:child_id>/",
        views.delete_child,
        name="delete_child",
    ),
]
