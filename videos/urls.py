from django.urls import path
from . import views

urlpatterns = [
    path('', views.stream_videos, name ='stream_videos'),
    path('stream/<int:video_id>/', views.stream_video, name='stream_video'),
]