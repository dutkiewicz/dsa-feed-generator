from django.core.management.base import BaseCommand
from api import models


class Command(BaseCommand):
    help = 'Clears all generated files and model.Feeds'

    def handle(self, *args, **kwargs):
        models.Feed.objects.all().delete()
        self.stdout.write("Deleted all models and files!")
