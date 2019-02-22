from rest_framework import serializers
from api import models


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Feed
        fields = ('pk', 'url', 'file')
