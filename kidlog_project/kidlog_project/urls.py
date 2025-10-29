from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("kidlog.urls")),
    path("accounts/", include("accounts.urls")),
    path("ai_chat/", include("ai_chat.urls")),
    path("diary/", include("diary.urls")),
    path("child_selection/", include("child_selection.urls")),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
