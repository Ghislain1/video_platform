from . import views
from django.urls import path


app_name = "videos"

urlpatterns = [
    path("main-admin/", views.admin_dashboard, name="admin_dashboard"),
    path("main-admin/videos/add/", views.add_video, name="add_video"),
]