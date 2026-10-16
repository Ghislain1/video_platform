from django.conf import settings
from django.core.files.storage import FileSystemStorage


private_video_storage = FileSystemStorage(
    location=settings.BASE_DIR / "private_media",
    base_url="/private-video-files/"
)