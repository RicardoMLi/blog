from django.db import models


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    # 注册和找回密码均要使用验证码
    send_type = models.CharField(choices=(('register', '注册'), ('forget', '找回密码'), ('modify', '修改邮箱')), max_length=10,
                                 verbose_name='验证码类型')
    send_time = models.DateTimeField(auto_now_add=True, verbose_name='发送时间')

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code


class Quote(models.Model):
    quote = models.CharField(max_length=200, verbose_name='名言')
    author = models.CharField(max_length=30, verbose_name='作者')

    class Meta:
        verbose_name = '名言'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.quote

