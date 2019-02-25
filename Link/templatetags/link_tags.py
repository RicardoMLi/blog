from django import template

from ..models import Links

register = template.Library()


@register.simple_tag()
def get_links_by_year_and_month(date):
    links = Links.objects.filter(add_time__year=date.year, add_time__month=date.month)
    days = []
    for link in links:
        if link.add_time.day not in days:
            days.append(link.add_time.day)

    # 日期为键，值为创建时间为该日期的友链列表
    links_dict = {}
    for day in days:
        links_dict[day] = []
        for link in links:
            if link.add_time.day == day:
                links_dict[day].append(link)

    return links_dict