from django import forms
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=3)
    email = forms.EmailField()
    password = forms.CharField(max_length=18, min_length=5)
    password_again = forms.CharField(max_length=18, min_length=5)

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已被注册')

        return email

    def clean_password_again(self):
        password = self.cleaned_data.get('password')
        password_again = self.cleaned_data.get('password_again')

        if password != password_again:
            raise forms.ValidationError('两次输入的密码不一致')

        return password_again


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if not User.objects.filter(Q(username=username) | Q(email=username)).exists():
            raise forms.ValidationError('用户名不存在')

        user = authenticate(username=username, password=password)
        if user is None:
            if User.objects.filter(email=username).exists():
                username = User.objects.get(email=username).username
                user = authenticate(username=username, password=password)
                if user:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
            raise forms.ValidationError('用户名或密码错误')
        else:
            self.cleaned_data['user'] = user

        return self.cleaned_data



