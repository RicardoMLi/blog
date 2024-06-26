import xadmin

from .models import Category, Message, Notice


class CategoryAdmin(object):
    list_display = ['name', 'parent_id', 'link']
    search_fields = ['name', 'parent_id', 'link']
    list_filter = ['name', 'parent_id', 'link']


class MessageAdmin(object):
    list_display = ['user', 'message', 'created_time', 'parent']
    search_fields = ['user', 'message', 'parent']
    list_filter = ['user', 'message', 'created_time', 'parent']


class NoticeAdmin(object):
    list_display = ['index', 'content', 'created_time']
    search_fields = ['index', 'content']
    list_filter = ['index', 'content', 'created_time']


xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(Message, MessageAdmin)
xadmin.site.register(Notice, NoticeAdmin)