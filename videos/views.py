from django.shortcuts import render
from videos.models import Video
from payments.models import Purchase
import os
from django.http import FileResponse, HttpResponseForbidden

# Create your views here.
def stream_videos(request):
    videos = Video.objects.all()

    purchased_video_ids = []

    if request.user.is_authenticated:
        purchased_video_ids = Purchase.objects.filter(
            user = request.user,
            is_paid= True
        ).values_list('video_id', flat=True)
    return render(request, 'videos/video_list.html', {
        'videos': videos,
        'purchased_video_ids': list(purchased_video_ids)
    })

def stream_video(request, video_id):
    video = Video.objects.get(id=video_id)

    # check if user paid
    has_access = False

    if request.user.is_authenticated:
        has_access = Purchase.objects.filter(
            user = request.user,
            video = video,
            is_paid =True
        ).exists()
    if has_access:
        file_path = video.video_file.path
    else:
        file_path = video.video_prev.path
    
    # Get file path
    file_path = video.video_file.path
    return FileResponse(open(file_path, 'rb', content_type='video/mp4'))
    