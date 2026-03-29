from http.client import HTTPResponse
from django.shortcuts import render, get_object_or_404
from .models import Video
from payments.models import Purchase
import os
from django.http import FileResponse, HttpResponseForbidden, StreamingHttpResponse

# Create your views here.
def video_list(request):
    videos = Video.objects.all()
    return render(request, 'videos/video_list.html', {'videos': videos})


# -------- videos Stream (source) ------
def stream_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    file_path = video.video_file.path
    file_size = os.path.getsize(file_path)

    # Check access
    has_access = False
    if request.user.is_authenticated:
        has_access = Purchase.objects.filter(
            user=request.user,
            video=video,
            is_paid=True
        ).exists()

    range_header = request.headers.get('Range', None)

    if not range_header:
        return FileResponse(open(file_path, 'rb'), content_type='video/mp4')

    # 🔥 Clean range
    range_value = range_header.lower().replace('bytes', '').replace('=', '').strip()
    start_str, end_str = range_value.split('-')

    start = int(start_str) if start_str.strip().isdigit() else 0
    end = int(end_str) if end_str.strip().isdigit() else file_size - 1

    # Preview limit
    preview_bytes = int(file_size * 0.2)

    if not has_access:
        end = min(end, preview_bytes)

    end = min(end, file_size - 1)
    length = end - start + 1

    file = open(file_path, 'rb')
    file.seek(start)

    response = FileResponse(file, status=206, content_type='video/mp4')
    response['Content-Length'] = str(length)
    response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
    response['Accept-Ranges'] = 'bytes'

    return response

#----------- video Details -------------
def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    has_access = False
    if request.user.is_authenticated:
        has_access = Purchase.objects.filter(
            user=request.user,
            video=video,
            is_paid = True
        ).exists()
    return render(render, 'videos/video_detail.html', {
        'video': video,
        'has_access': has_access
    })

# ------- Payment PlaceHolder ------
def pay_video(request, video_id):
    # implemet payment logic will be here 
    return HTTPResponse("Payment page for video {}".format(video_id))