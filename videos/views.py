from django.shortcuts import render
from videos.models import Video

# Create your views here.
def video_list(request):
    videos = Video.objects.all()
    return render(request, 'videos/video_list.html', {'videos': videos})