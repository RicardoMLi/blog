from django.views.generic import View
from django.shortcuts import render
from pure_pagination import Paginator, PageNotAnInteger

from Blog.models import Banner
from Blog.models import Blog
from utils.RenderWrite import render_template


class IndexView(View):

    def get(self, request):
        context = {}
        all_blogs = Blog.objects.all().order_by('-created_time')
        hot_blogs = Blog.objects.all().order_by('-click_num')[:5]

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_blogs, 3, request=request)

        blogs = p.page(page)

        context['blogs'] = blogs
        context['hot_blogs'] = hot_blogs
        context['name'] = '首页'
        context['banners'] = Banner.objects.all().order_by('index')
        return render_template(request, 'index.html', context)


class LoveView(View):

    def get(self, request):

        return render(request, 'love.html')