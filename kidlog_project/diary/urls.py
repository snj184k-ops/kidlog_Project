from django.urls import path
from . import views

urlpatterns = [
    path("<int:child_id>/", views.diary_list, name="diary_list"),
    path("<int:child_id>/add/", views.diary_add, name="diary_add"),
    path("<int:child_id>/edit/<int:pk>/", views.diary_edit, name="diary_edit"),
    path("<int:child_id>/delete/<int:pk>/", views.diary_delete, name="diary_delete"),
]
