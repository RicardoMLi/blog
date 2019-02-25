from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=20, verbose_name='技能')
    master_rate = models.IntegerField(verbose_name='技能掌握比')

    class Meta:
        verbose_name = '技能掌握'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Profile(models.Model):
    name = models.CharField(max_length=10, verbose_name='名字')
    desc = models.TextField(verbose_name='简介')
    skill = models.ForeignKey(Skill, verbose_name='技能', on_delete=models.CASCADE)
    address = models.CharField(max_length=100, verbose_name='地址')
    occupation = models.CharField(max_length=20, verbose_name='职业', default='学生')
    company = models.CharField(max_length=20, verbose_name='公司', default='')

    class Meta:
        verbose_name = '我的信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
