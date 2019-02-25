from django.shortcuts import render
from django.db.models import Count

from Category.models import Category
from Blog.models import Blog, Tag
from Comment.models import Comment
from Link.models import Links


# 将首页分类数据抽离出来
def render_template(request, template_name, context=None, content_type=None, status=None, using=None):
    parent_categories = Category.objects.filter(parent_id=None)

    current_click = request.COOKIES.get('current_click', '')
    if current_click:
        current_click = current_click.split('_')
        current_click_blogs = [Blog.objects.get(id=int(index)) for index in current_click]
        # 猜你喜欢
        liked_blogs = []
        for blog in current_click_blogs:
            blogs = Blog.objects.filter(tag=blog.tag)
            for liked_blog in blogs:
                if liked_blogs.count(liked_blog) == 0:
                    liked_blogs.append(liked_blog)
    else:
        current_click_blogs = []
        liked_blogs = Blog.objects.all().order_by('-like_num')

    # 标签云
    tags = Tag.objects.all()

    # 日期归档
    blog_dates = Blog.objects.dates('created_time', 'month', 'DESC').annotate(type_blog_date=Count('created_time'))
    blog_dates_dict = {}
    for i in range(0, len(blog_dates)-1, 2):
        blog_dates_dict[blog_dates[i]] = blog_dates[i+1]

    # 最新评论
    lastest_comments = Comment.objects.filter(parent=None).order_by('-created_time')[:5]

    # 友链
    links = Links.objects.all()

    if isinstance(context, dict):
        context['parent_categories'] = parent_categories
        context['current_click_blogs'] = current_click_blogs
        context['liked_blogs'] = liked_blogs[:5]
        context['tags'] = tags
        context['lastest_comments'] = lastest_comments
        context['blog_dates'] = blog_dates_dict
        context['links'] = links
    else:
        context = {
            'parent_categories': parent_categories,
            'current_click_blogs': current_click_blogs,
            'liked_blogs': liked_blogs[:5],
            'tags': tags,
            'lastest_comments': lastest_comments,
            'blog_dates': blog_dates_dict,
            'links': links
        }
    return render(
        request=request,
        template_name=template_name,
        context=context,
        content_type=content_type,
        status=status,
        using=using
    )