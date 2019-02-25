from django.views.generic import View

from .models import Links
from utils.RenderWrite import render_template


class LinksView(View):

    def get(self, request):
        link_dates = Links.objects.dates('add_time', 'month', 'DESC')
        context = {
            'name': '友情链接',
            'link_dates': link_dates,
        }

        return render_template(request, 'link/links.html', context)
