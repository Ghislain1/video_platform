from django.db import models

# Create your models here.

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_file = models.FileField(upload_to='videos/')
    preview_duration = models.IntegerField()
    price = models.DecimalField(max_digits = 6, decimal_places=2)

    def __str__(self):
        return self.title