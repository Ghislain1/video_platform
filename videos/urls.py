from django.urls import path
from . import views

urlpatterns = [
    path('', views.video_list, name ='video_list'),
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),
    path('stream/<int:video_id>/', views.stream_video, name='stream_video'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/create/', views.create_video, name='create_video'),
    path('dashboard/edit/<int:video_id>/', views.edit_video, name='edit_video'),
    path('dashboard/delete/<int:video_id>/', views.delete_video, name='delete_video'),
]