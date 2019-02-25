from django import forms
from django.contrib.auth.models import User

from Blog.models import Blog


class CommentForm(forms.Form):
    user_id = forms.IntegerField()
    blog_id = forms.IntegerField()
    comment = forms.CharField()

    def clean_user_id(self):
        user_id = self.cleaned_data.get('user_id', '')

        if user_id == '':
            raise forms.ValidationError("用户尚未登录")

        if not User.objects.filter(id=user_id).exists():
            raise forms.ValidationError("用户不存在")

        self.cleaned_data['user'] = User.objects.get(id=user_id)
        return user_id

    def clean_blog_id(self):
        blog_id = self.cleaned_data.get('blog_id', '')

        if blog_id == '' or not Blog.objects.filter(id=blog_id).exists():
            raise forms.ValidationError("博客不存在")

        self.cleaned_data['blog'] = Blog.objects.get(id=blog_id)
        return blog_id

    def clean_comment(self):
        comment = self.cleaned_data.get('comment', '')

        if comment == '':
            raise forms.ValidationError("评论内容不能为空")

        return comment
