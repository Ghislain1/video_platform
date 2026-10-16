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
    path("main-admin/categories/", views.manage_categories, name="manage_categories",),
    path("main-admin/categories/add/", views.add_category, name="add_category",),
    path("main-admin/categories/<int:category_id>/edit/", views.edit_category, name="edit_category",),
    path("main-admin/categories/<int:category_id>/delete/", views.delete_category, name="delete_category",),

    path("", views.public_video_library, name="public_library"),
    path("video/<int:video_id>/", views.public_video_detail, name="video_detail"),

    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("account/", views.account_view, name="account"),
]