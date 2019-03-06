import threading
from api import models
from api import serializers
from api import tasks
from rest_framework import viewsets, views, permissions, authentication
from django.views import View
from django.shortcuts import get_object_or_404, HttpResponse


# Create your views here.

class FeedApiView(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, )

    queryset = models.Feed.objects.all()
    serializer_class = serializers.FeedSerializer


class DSAFeedApiView(views.APIView):

    def post(self, request, format=None):
        if request.data.get('url'):
            url = request.data['url']
            feed = models.Feed(url=url)
            feed.save()
            threading.Thread(target=tasks.generate_feed_file, args=(feed.pk, feed.url)).start()
            
            return views.Response({'status': 'ok', 'id': feed.pk})
        else:
            return views.Response(status=400, data={'error': 'URL must be provided!'})

    def get(self, request, id=None, format=None):
        feed = models.Feed.objects.get(pk=id)
        if feed.file.name:
            serialized = serializers.FeedSerializer(feed)
            return views.Response({"status": "done", "feed": serialized.data})
        else:
            return views.Response({"status": "processing"})

class DownloadFileView(View):

    def get(self, request, *args, **kwargs):
        feed = get_object_or_404(models.Feed, pk=self.kwargs['id'])
        response = HttpResponse(feed.file, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=dsa-feed.csv'

        return response


