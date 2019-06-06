from django.db import models
from django.utils import timezone


# Create your models here.

class Feed(models.Model):
    url = models.URLField(null=True)
    file = models.FileField(null=True, blank=True)
    is_processed = models.BooleanField(default=False)
    exception = models.CharField(max_length=500, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.url
