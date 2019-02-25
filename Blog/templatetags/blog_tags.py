from django import template

from ..models import Blog

register = template.Library()


@register.simple_tag()
def get_blogs_by_year_and_month(date):
    blogs = Blog.objects.filter(created_time__year=date.year, created_time__month=date.month)
    days = []
    for blog in blogs:
        if blog.created_time.day not in days:
            days.append(blog.created_time.day)

    # 日期为键，值为创建时间为该日期的博客列表
    blog_dict = {}
    for day in days:
        blog_dict[day] = []
        for blog in blogs:
            if blog.created_time.day == day:
                blog_dict[day].append(blog)

    return blog_dict


@register.simple_tag()
def get_blogs_by_tag(id):

    return Blog.objects.filter(tag_id=id)

