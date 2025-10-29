from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/<int:child_id>/", views.dashboard, name="dashboard"),
    path(
        "baby_record/<int:child_id>/",
        views.baby_record_overview,
        name="baby_record_overview",
    ),
    path(
        "baby_record_add/<int:child_id>/",
        views.baby_record_add,
        name="baby_record_add",
    ),
]
