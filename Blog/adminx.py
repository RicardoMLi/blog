import xadmin

from .models import Blog, Tag, Banner


class TagAdmin(object):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['name']


class BlogAdmin(object):
    list_display = ['title', 'introduction', 'click_num', 'like_num', 'author', 'content', 'created_time', 'category', 'tag', 'image', 'share_times']
    search_fields = ['title', 'introduction', 'click_num', 'like_num', 'author', 'content', 'category', 'tag', 'share_times']
    list_filter = ['title', 'introduction', 'click_num', 'like_num','author', 'content', 'created_time', 'category', 'tag', 'image', 'share_times']


class BannerAdmin(object):
    list_display = ['index', 'blog', 'image']
    search_fields = ['index', 'blog', 'image']
    list_filter = ['index', 'blog', 'image']


xadmin.site.register(Blog, BlogAdmin)
xadmin.site.register(Tag, TagAdmin)
xadmin.site.register(Banner, BannerAdmin)
