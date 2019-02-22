from api import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


@receiver(post_delete, sender=models.Feed)
def delete_file(sender, instance, **kwargs):
    instance.file.delete()
