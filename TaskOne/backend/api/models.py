from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=100)
    url=models.CharField(max_length=300)
    bucket_id=models.CharField(max_length=100,blank=True)
    created_at=models.DateTimeField(auto_now_add=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name="videos")
    

    def __str__(self) -> str:
        return self.title