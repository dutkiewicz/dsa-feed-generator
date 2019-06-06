import threading

from api import models
from api import tasks
from django.shortcuts import get_object_or_404, HttpResponse
from django.views import View
from rest_framework import views, status


# Create your views here.

class FeedApiView(views.APIView):

    def post(self, request, format=None):
        if request.data.get('url'):
            feed = models.Feed(url=request.data['url'])
            feed.save()
            threading.Thread(target=tasks.generate_feed_file, args=(feed.pk, feed.url)).start()

            return views.Response(status=status.HTTP_202_ACCEPTED,
                                  headers={
                                      'Location': '/api/v1/feeds/{}/file'.format(feed.pk),
                                      'Operation-Location': '/api/v1/feeds/{}'.format(feed.pk)
                                  },
                                  data={
                                      'status': 'accepted',
                                      'id': feed.pk
                                  })
        else:
            return views.Response(status=status.HTTP_400_BAD_REQUEST,
                                  data={'error': 'URL must be provided!'})

    def get(self, request, id=None, format=None):
        feed = get_object_or_404(models.Feed, pk=id)

        if feed.is_processed:
            return views.Response(status=status.HTTP_201_CREATED,
                                  headers={"Location": "/api/v1/feeds/{}/file".format(feed.pk)},
                                  data={
                                      "id": feed.pk,
                                      "status": "finished",
                                      "location": "/api/v1/feeds/{}/file".format(feed.pk)
                                  })
        else:
            return views.Response({"id": feed.pk, "status": "processing"})


class DownloadFileView(View):

    def get(self, request, id=None, *args, **kwargs):
        feed = get_object_or_404(models.Feed, pk=id)
        response = HttpResponse(feed.file, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=dsa-page-feed.csv'

        return response
