from django.shortcuts import render
from videos.models import Video
from payments.models import Purchase

# Create your views here.
def video_list(request):
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
