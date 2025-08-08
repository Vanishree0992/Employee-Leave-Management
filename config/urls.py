from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),  # login/logout
    path("accounts/", include("accounts.urls")),  # if you made a custom registration view
    path("", include("leave.urls")),  # leave app urls
]
