from django.db import models


class Links(models.Model):
    name = models.CharField(max_length=30, verbose_name='博客名称')
    link = models.CharField(max_length=50, verbose_name='网站链接')
    add_time = models.DateField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '友链'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
