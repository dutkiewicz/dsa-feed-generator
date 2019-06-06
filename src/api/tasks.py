import csv
import os

from django.conf import settings

from api.modules.xml_parser import FeedParser
from api.models import Feed


def generate_feed_file(model_id: int, url: str) -> None:
    feed = Feed.objects.get(pk=model_id)

    try:
        xml_feed = FeedParser(url)
    except Exception as e:
        feed.exception = e
        feed.save()
        raise

    file = os.path.join(settings.MEDIA_ROOT, 'feed_id_{}.csv'.format(model_id))

    with open(file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Page URL'])

        for item in xml_feed:
            writer.writerow(item['link'])


    feed.file = file
    feed.is_processed = True
    feed.save()
