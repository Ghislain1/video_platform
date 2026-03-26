from django.db import models
from django.contrib.auth.models import User
from videos.models import Video

# Create your models here.
class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    stripe_session_id = models.CharField(max_length=255)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.video}"