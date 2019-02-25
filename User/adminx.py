import xadmin

from .models import EmailVerifyRecord, Quote


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class QuoteAdmin(object):
    list_display = ['quote', 'author']
    search_fields = ['quote', 'author']
    list_filter = ['quote', 'author']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Quote, QuoteAdmin)