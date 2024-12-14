from django.conf import settings
from django.db import models
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='intruder_image/%Y/%m/%d/', default='intruder_image/default_error.png')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

# class DetectionRecord(models.Model):  #12.14 add
#     detected_at = models.DateTimeField(auto_now_add=True)  # 自动记录检测时间
#     category = models.CharField(max_length=100)
#     count = models.IntegerField(default=1)

#     def save(self, *args, **kwargs):
#         if self.category.lower() == "person":
#             super().save(*args, **kwargs)
#         else:
#             print(f"Category '{self.category}' is not allowed. Record not saved.")



class DetectionRecord(models.Model):  # 12.14 add
    detected_hour = models.DateTimeField(default=timezone.now)
    count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)