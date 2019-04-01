from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed

from Blog.models import Blog


class BlogFeedView(Feed):
    feed_type = Rss201rev2Feed
    link = '/feed/'
    title = '念旧博客-RSS'
    description = '不畏将来，不念过往'

    def items(self):
        return Blog.objects.order_by('-created_time')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.introduction

    def item_link(self, item):
        return item.get_absolute_url()
