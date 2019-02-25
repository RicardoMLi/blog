from django.shortcuts import render
from pure_pagination import PageNotAnInteger, Paginator, EmptyPage
from django.http import JsonResponse
from django.views.generic import View

from .models import Blog, Tag

from Comment.models import Comment
from Category.models import Category
from utils.RenderWrite import render_template


class BlogView(View):

    def get(self, request, blog_id):
        if not isinstance(blog_id, int):
            return render(request, '404.html', {})
        if not Blog.objects.filter(id=blog_id).exists():
            return render(request, '404.html', {})
        blog = Blog.objects.get(id=blog_id)
        blog.click_num += 1
        blog.save()

        # 查找本篇博客前后篇博客
        pre_blog = Blog.objects.filter(id__lt=blog.id).order_by('-id')[0] if Blog.objects.filter(id__lt=blog.id).order_by('-id') else None
        next_blog = Blog.objects.filter(id__gt=blog.id).order_by('id')[0] if Blog.objects.filter(id__gt=blog.id).order_by('id') else None

        # 查找本篇博客评论
        blog_comments = Comment.objects.filter(blog_id=blog.id)
        num_of_people = len(list(set(blog_comments)))

        # 查找父级标题
        category = Category.objects.get(id=blog.category_id)
        parent_category = Category.objects.get(id=category.parent_id)

        # 将用户最近浏览的博客加入cookie
        blog_id = str(blog_id)
        current_click = request.COOKIES.get('current_click', '')
        if current_click == '':
            current_click += '{0}'.format(blog_id)
        else:
            l = current_click.split('_')
            if l.count(blog_id) == 0:
                if len(l) >= 3:
                    l.pop()
                l.insert(0, blog_id)
            current_click = '_'.join(l)

        context = {
            'name': parent_category.name,
            'blog': blog,
            'comments': blog_comments,
            'num_of_people': num_of_people,
            'pre_blog': pre_blog,
            'next_blog': next_blog
        }
        res = render_template(request, 'blog/blog.html', context)
        res.set_cookie('current_click', current_click)

        return res


# 分享博客
class ShareBlogView(View):

    def get(self, request):
        id = request.GET.get('id', '')
        return_data = {}

        if id == '':
            return_data['status'] = 'fail'
            return_data['msg'] = '博客id错误'
            return JsonResponse(return_data)

        try:
            id = int(id)
        except ValueError:
            return_data['status'] = 'fail'
            return_data['msg'] = '博客id错误'
            return JsonResponse(return_data)

        blog = Blog.objects.filter(id=id)
        if not blog.exists():
            return_data['status'] = 'fail'
            return_data['msg'] = '博客id错误'
            return JsonResponse(return_data)

        blog = blog[0]
        blog.share_times += 1
        blog.save()

        return_data['status'] = 'success'
        return_data['msg'] = blog.share_times

        return JsonResponse(return_data)


# 博客日期归档
class BlogWithDateView(View):

    def get(self, request, year, month):
        if month > 12 or month < 0:
            return render(request, '404.html', {})

        all_blogs = Blog.objects.filter(created_time__year=year, created_time__month=month)
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_blogs, 3, request=request)

        blogs = p.page(page)
        context = {'blogs': blogs, 'name': '日期归档'}

        return render_template(request, 'category/category.html', context)


# 过去所有历史文章(以文章日期分类)
class HistoryBlogsView(View):

    def get(self, request):
        blog_dates = Blog.objects.dates('created_time', 'month', 'DESC')
        context = {
            'blog_dates': blog_dates,
            'name': '历史文章'
        }
        return render_template(request, 'blog/blog_date.html', context)


class AllTagsView(View):

    def get(self, request):
        tags = Tag.objects.all()
        context = {
            'name': '标签云',
            'tags': tags
        }
        return render_template(request, 'blog/blog_tags.html', context)


class TagView(View):

    def get(self, request, tag_name):
        if not isinstance(tag_name, str) or tag_name == '':
            return render(request, '404.html', {})

        tag = Tag.objects.filter(name=tag_name)
        if not tag.exists():
            return render(request, '404.html', {})

        all_blogs = Blog.objects.filter(tag=tag[0])

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_blogs, 3, request=request)

        blogs = p.page(page)

        context = {'blogs': blogs, 'name': tag_name}
        return render_template(request, 'category/category.html', context)


class LikeAddView(View):
    def post(self, request):
        blog_id = request.POST.get('um_id', '')
        if blog_id == '':
            return render(request, '404.html', {})
        try:
            blog_id = int(blog_id)
        except ValueError:
            return render(request, '404.html', {})

        blog = Blog.objects.filter(id=blog_id)
        if not blog.exists():
            return render(request, '404.html', {})

        blog = blog[0]
        blog.like_num += 1
        blog.save()

        return JsonResponse({'like_count': blog.like_num})
