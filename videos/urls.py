from . import views
from django.urls import path


app_name = "videos"

urlpatterns = [
    path("main-admin/", views.admin_dashboard, name="admin_dashboard"),
    path("main-admin/videos/add/", views.add_video, name="add_video"),
    path("main-admin/videos/", views.manage_videos, name="manage_videos",),
    path("main-admin/videos/<int:video_id>/edit/", views.edit_video, name="edit_video",),
    path("main-admin/videos/<int:video_id>/toggle-publication/", views.toggle_video_publication, name="toggle_video_publication",),
    path("main-admin/videos/<int:video_id>/delete/", views.delete_video, name="delete_video",),
]