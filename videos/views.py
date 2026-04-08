from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import VideoForm
from .models import Video
from payments.models import Purchase
import os
from django.http import FileResponse, HttpResponseForbidden, StreamingHttpResponse
from django.contrib.admin.views.decorators import staff_member_required

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

# ----- ADMIN VIEWS SIDE -----------
@staff_member_required  # this makes only users with 'is_staff=True' can access, others get redirected to login
def admin_dashboard(request):
    videos = Video.objects.all()

    return render(request, 'videos/admin_dashboard.html', { 'videos': videos})

# ------add video -------
@staff_member_required
def create_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
            form = VideoForm()
    return render(request, 'videos/form.html', {'form': form})

# ------ edit video ---------
@staff_member_required
def edit_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = VideoForm(instance=video)
    return render(request, 'videos/form.html', {'form': form})
# ----- delete video ------
@staff_member_required
def delete_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    video.delete()
    return redirect('admin_dashboard')


# ------- Payment PlaceHolder ------
def pay_video(request, video_id):
    # implement payment logic will be here
    return HttpResponse("Payment page for video {}".format(video_id))