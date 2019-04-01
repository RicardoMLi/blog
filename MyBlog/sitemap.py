from django.contrib.sitemaps import Sitemap
from Blog.models import Blog


class BlogSiteMap(Sitemap):
    changefreq = 'monthly'
    property = 0.5

    def items(self):
        return Blog.objects.order_by('-created_time')

    def lastmod(self, obj):
        return obj.created_time

    def location(self, obj):
        return obj.get_absolute_url()