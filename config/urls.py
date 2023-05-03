from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as doc_url

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("app.costs.urls")),
    path("api/v1/auth/", include("app.auth.urls")),
]

urlpatterns += doc_url
