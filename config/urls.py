from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("u/", include("apps.accounts.urls")),
    path("api/", include("apps.core.urls")),
    path("", include("apps.core.urls_views")),
]
