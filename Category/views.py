from threading import Thread
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.generic import View
from pure_pagination import Paginator, PageNotAnInteger, EmptyPage

from Category.models import Category
from Blog.models import Blog
from MyBlog.settings import PER_PAGE_MESSAGES
from utils.send_email import send_email
from utils.RenderWrite import render_template
from .models import Message, Notice


def get_root_blogs(id):
    child_categories = Category.objects.filter(parent_id=id)
    all_blogs = []
    for child_category in child_categories:
        all_blogs.extend(Blog.objects.filter(category_id=child_category.id))

    return all_blogs


class FindParentView(View):

    def get(self, request):
        id = request.GET.get('id', '')
        is_parent = request.GET.get('is_parent', '')
        return_data = {}

        if id == '':
            return_data['status'] = 'fail'
            return_data['msg'] = 'id不能为空'
            return JsonResponse(return_data)

        category = Category.objects.filter(id=id)

        if not category.exists():
            return_data['status'] = 'fail'
            return_data['msg'] = 'id错误'
            return JsonResponse(return_data)

        parent_category = Category.objects.get(id=category[0].parent_id)
        if is_parent == 'false':
            return_data['status'] = 'success'
            return_data['msg'] = '/category/{0}/{1}/'.format(parent_category.link,category[0].link)
        elif is_parent == 'true':
            return_data['status'] = 'success'
            return_data['msg'] = '/category/{0}/'.format(parent_category.link)
        else:
            return_data['status'] = 'fail'
            return_data['msg'] = '发生错误'

        return JsonResponse(return_data)


class MyDailyView(View):

    def get(self, request):
        all_blogs = get_root_blogs(1)

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_blogs, 3, request=request)

        blogs = p.page(page)
        context = {'name': '我的日常', 'blogs': blogs}

        return render_template(request, 'category/category.html',context)


class MyDailyExtendView(View):

    def get(self, request, router):
        context = {}
        if router == 'jottings':
            all_blogs = Blog.objects.filter(category_id=6)
            context['name'] = '个人随笔'
        elif router == 'notes':
            all_blogs = Blog.objects.filter(category_id=7)
            context['name'] = '个人笔记'
        else:
            return render(request, '404.html', {})

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_blogs, 3, request=request)

        blogs = p.page(page)
        context['blogs'] = blogs
        return render_template(request, 'category/category.html', context)


class TechnologyView(View):

    def get(self, request):
        all_blogs = get_root_blogs(2)

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_blogs, 3, request=request)

        blogs = p.page(page)
        context = {'name': '技术分享', 'blogs': blogs}

        return render_template(request, 'category/category.html', context)


class TechnologyExtendView(View):

    def get(self, request, router):
        context = {}
        if router == 'python':
            all_blogs = Blog.objects.filter(category_id=8)
            context['name'] = 'Python'
        elif router == 'java':
            all_blogs = Blog.objects.filter(category_id=9)
            context['name'] = 'Java'
        elif router == 'cc':
            all_blogs = Blog.objects.filter(category_id=10)
            context['name'] = 'C/C++'
        elif router == 'javascript':
            all_blogs = Blog.objects.filter(category_id=11)
            context['name'] = 'JavaScript'
        elif router == 'other':
            all_blogs = Blog.objects.filter(category_id=12)
            context['name'] = 'Other'

        else:
            return render(request, '404.html', {})

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_blogs, 3, request=request)

        blogs = p.page(page)
        context['blogs'] = blogs

        return render_template(request, 'category/category.html', context)


class MessageView(View):

    def get(self, request):
        context = {}
        notices = Notice.objects.all().order_by('index')
        all_messages = Message.objects.all()
        root_messages = [message for message in all_messages if message.is_root_node()]
        messages = [node.get_descendants(include_self=True) for node in root_messages]
        num_of_people = len(list(set(all_messages)))

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(messages, PER_PAGE_MESSAGES, request=request)
        page_messages = p.page(page)

        context['messages'] = page_messages
        context['notices'] = notices
        context['name'] = '留言交流'
        context['num_of_people'] = num_of_people

        return render_template(request, 'category/message.html', context)

    def post(self, request):
        # 当前用户id
        current_user_id = request.POST.get('current_user_id','')
        comment = request.POST.get('comment', '')
        # 留言用户id
        to_user_id = request.POST.get('to_user_id', '')
        # 留言id
        to_message_id = request.POST.get('to_message_id', '')

        return_data = {}

        # 判断是否是留言还是回复留言
        if not all((to_user_id, to_message_id)):
            # 留言
            if not all((current_user_id, comment)):
                return_data['status'] = 'fail'
                return_data['msg'] = '用户未登录或留言为空'
                return JsonResponse(return_data)

            user = User.objects.filter(id=int(current_user_id))
            if not user.exists():
                return_data['status'] = 'fail'
                return_data['msg'] = '用户未登录,请先登录后再留言'
                return JsonResponse(return_data)

            message = Message()
            message.user = user[0]
            message.message = comment
            message.parent = None
            message.save()

            # 多进程发送邮件
            t = Thread(target=send_email, args=(message.user.email, 'message', message.id))
            t.start()

            return_data['status'] = 'success'
            return_data['msg'] = {
                'message': comment,
                'time': message.created_time.timestamp(),
                'username': message.user.username,
                'message_id': message.id,
                # 此留言用户id
                'user_id': message.user.id,
                # 标识评论标签id
                'comment': 'comment_{0}'.format(message.id)
            }
            return JsonResponse(return_data)
        else:
            # 回复留言
            if not all((current_user_id, comment)):
                return_data['status'] = 'fail'
                return_data['msg'] = '用户未登录或留言为空'
                return JsonResponse(return_data)

            current_user = User.objects.filter(id=int(current_user_id))
            to_message = Message.objects.filter(id=int(to_message_id))

            if not all((current_user, to_message)):
                return_data['status'] = 'fail'
                return_data['msg'] = '留言出错'
                return JsonResponse(return_data)

            message = Message()
            message.user = current_user[0]
            message.message = comment
            message.parent = to_message[0]
            message.save()

            # 多进程发送邮件
            t = Thread(target=send_email, args=(message.user.email, 'return_message', message.id))
            t.start()

            return_data['status'] = 'success'
            return_data['msg'] = {
                'reply': 'yes',
                'message': comment,
                'time': message.created_time.timestamp(),
                'username': message.user.username,
                'message_id': message.id,
                # 此留言标签id
                'message_comment_id': 'comment_{0}'.format(message.id),
                # 此留言用户id
                'user_id': message.user.id,
                # 标识评论标签id
                'comment': 'comment_{0}'.format(to_message[0].id)
            }

            return JsonResponse(return_data)


class DonationView(View):

    def get(self, request):
        context = {'name': '赞助作者'}
        return render_template(request, 'category/donation.html', context)


class ShareView(View):

    def get(self, request):
        context = {}
        all_blogs = get_root_blogs(5)

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_blogs, 3, request=request)

        blogs = p.page(page)
        context['blogs'] = blogs
        context['name'] = '福利专区'
        return render_template(request, 'category/category.html', context)


class ShareExtendView(View):

    def get(self, request, router):
        context = {}
        all_blogs = []
        if router == 'download':
            all_blogs = Blog.objects.filter(category_id=13)
            context['name'] = '资源下载'

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_blogs, 3, request=request)
        blogs = p.page(page)
        context['blogs'] = blogs

        return render_template(request, 'category/category.html', context)
