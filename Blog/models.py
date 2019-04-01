from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

from Category.models import Category


class Tag(models.Model):
    name = models.CharField(max_length=20, verbose_name='标签')

    class Meta:
        verbose_name = '标签管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_tag_blog(self):
        return Blog.objects.filter(tag=self).count()


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='标题')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='作者')
    category = models.ForeignKey(Category, verbose_name='博客类型', on_delete=models.DO_NOTHING, null=True)
    tag = models.ForeignKey(Tag, verbose_name='标签', null=True, on_delete=models.DO_NOTHING)
    introduction = models.TextField(verbose_name='前言', default='')
    content = RichTextUploadingField(verbose_name='内容')
    click_num = models.IntegerField(default=0, verbose_name='点击数量')
    like_num = models.IntegerField(default=0, verbose_name='点赞数量')
    created_time = models.DateField(auto_now_add=True, verbose_name='日期')
    share_times = models.IntegerField(default=0, verbose_name='分享次数')
    image = models.ImageField(upload_to='blog/', verbose_name='博客图片', null=True, blank=True)

    class Meta:
        verbose_name = '博客'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    # 获取评论数量
    def get_comments_num(self):
        return self.comment_set.all().count()

    # 获取博客url
    def get_absolute_url(self):
        return '/blog/{0}'.format(self.id)


class Banner(models.Model):
    index = models.IntegerField(verbose_name='轮播顺序')
    blog = models.ForeignKey(Blog, verbose_name='轮播博客', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='banner/', max_length=100, verbose_name='图片')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.blog.title



