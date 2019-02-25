import xadmin

from .models import Links


class LinksAdmin(object):
    list_display = ['name', 'link', 'add_time']
    search_fields = ['name', 'link']
    list_filter = ['name', 'link', 'add_time']


xadmin.site.register(Links, LinksAdmin)