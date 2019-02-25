import random
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import View
from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from .models import Quote, EmailVerifyRecord
from .forms import RegisterForm, LoginForm
from utils.send_email import send_email


class LoginView(View):

    def get(self, request):
        return render(request, 'user/login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        return_data = {}

        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            login(request, user)
            return_data['status'] = 'success'
            # 登录成功只能跳转到首页
            return_data['msg'] = request.GET.get('from',reverse('index'))
        else:
            return_data['status'] = 'fail'
            return_data['msg'] = login_form.errors

        return JsonResponse(return_data)


class LogoutView(View):

    def get(self, request):
        logout(request)
        # 跳转到上一个页面
        return redirect(request.GET.get('from',reverse('index')))


class CheckNameView(View):

    def get(self, request):
        name = request.GET.get('name')
        return_data = {}
        if name == '':
            return_data['status'] = 'fail'
            return_data['msg'] = '用户名为空'
            return JsonResponse(return_data)

        queryset = User.objects.filter(username=name)
        if queryset.exists():
            return_data['status'] = 'fail'
            return_data['msg'] = '用户名已存在'
        else:
            return_data['status'] = 'success'

        return JsonResponse(return_data)


class CheckEmailView(View):

    def get(self, request):
        email = request.GET.get('email')
        return_data = {}

        if email == '':
            return_data['status'] = 'fail'
            return_data['msg'] = '邮箱不能为空'
            return JsonResponse(return_data)

        queryset = User.objects.filter(email=email)
        if queryset.exists():
            return_data['status'] = 'fail'
            return_data['msg'] = '此邮箱已被注册'
        else:
            return_data['status'] = 'success'

        return JsonResponse(return_data)


class ActiveUserView(View):

    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = User.objects.filter(email=email)
                if user:
                    user = user[0]
                    user.is_active = True
                    user.save()
                    # 删除注册账号时发生的验证码记录
                    for record in EmailVerifyRecord.objects.filter(email=email, send_type='register'):
                        record.delete()
                    login(request, user)
                    return redirect('index')
        else:
            return render(request, 'user/active_fail.html', {})


class RegisterView(View):

    def get(self, request):
        context = {'register_form': RegisterForm()}

        return render(request, 'user/register.html', context)

    def post(self, request):
        context = {}
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            email = register_form.cleaned_data['email']
            # 发送激活邮件
            return_msg = send_email(email, 'register')
            if return_msg:
                # 用户注册
                username = register_form.cleaned_data['username']
                password = register_form.cleaned_data['password']
                user = User.objects.create_user(username, email, password)
                user.is_active = False
                return_data = {}
                return_data['status'] = 'success'
                return_data['return_url'] = '/user/register_success/'
                return JsonResponse(return_data)

            elif return_msg == '邮箱地址错误':
                context['title'] = '邮箱地址错误'
                return render(request, 'user/send_response.html', context)
            elif return_msg == '网络连接失败':
                context['title'] = '网络连接失败'
                return render(request, 'user/send_response.html', context)
            else:
                context['title'] = '服务器错误'
                return render(request, 'user/send_response.html', context)
        else:
            context['register_form'] = register_form
            return render(request, 'user/register.html', context)


class RegisterSuccessView(View):

    def get(self, request):
        context = {}
        quote = random.choice(Quote.objects.all())
        context['quote'] = quote
        return render(request, 'user/register_succ.html', context)
