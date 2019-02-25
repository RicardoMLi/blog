import xadmin

from .models import Comment


class CommentAdmin(object):
    list_display = ['user', 'content', 'created_time', 'parent', 'blog']
    search_fields = ['user', 'content', 'parent', 'blog']
    list_filter = ['user', 'content', 'created_time', 'parent', 'blog']


xadmin.site.register(Comment, CommentAdmin)