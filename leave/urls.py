from django.urls import path
from . import views

app_name = "leave"

urlpatterns = [
    path("", views.LeaveListView.as_view(), name="list"),
    path("create/", views.LeaveCreateView.as_view(), name="create"),
    path("<int:pk>/", views.LeaveDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.LeaveUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.LeaveDeleteView.as_view(), name="delete"),
    path("<int:pk>/action/", views.LeaveApproveRejectView.as_view(), name="action"),
]
