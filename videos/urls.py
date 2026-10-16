from . import views
from django.urls import path


app_name = "videos"

urlpatterns = [
    path("main-admin/", views.admin_dashboard, name="admin_dashboard"),
]