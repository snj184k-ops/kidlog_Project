from django.urls import path
from . import views

urlpatterns = [
    path("<int:child_id>/", views.chat_page, name="ai_chat"),
]
