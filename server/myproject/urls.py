from django.contrib import admin
from django.urls import include, path

from myproject import auth_views


urlpatterns = [
    path("", auth_views.health_check, name="home"),
    path("admin/", admin.site.urls),
    path("api/", include("myproject.auth_urls")),
    path("djangoapp/", include("myproject.coursera_urls")),
]
