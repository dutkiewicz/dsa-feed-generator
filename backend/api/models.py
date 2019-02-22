from django.db import models


# Create your models here.

class Feed(models.Model):
    url = models.URLField(null=True)
    file = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.url