from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey


class Category(models.Model):
    name = models.CharField(max_length=20, verbose_name='分类名称')
    parent_id = models.IntegerField(default=None, null=True, blank=True, verbose_name='父类id')
    link = models.CharField(max_length=20, default='', verbose_name='链接')

    class Meta:
        verbose_name = '分类管理'
        verbose_name_plural = verbose_name

    def get_child_set(self):
        return Category.objects.filter(parent_id=self.id)

    def has_child(self):
        return Category.objects.filter(parent_id=self.id) is not None

    def __str__(self):
        return self.name


class Message(MPTTModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    message = models.TextField(verbose_name='留言内容')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='留言时间')
    parent = TreeForeignKey('self', verbose_name='父节点', null=True, blank=True, related_name='children',
                            on_delete=models.CASCADE)

    class Meta:
        verbose_name = '留言管理'
        verbose_name_plural = verbose_name

    class MPTTMeta:
        parent_attr = 'parent'
        order_insertion_by = ['-created_time']

    # 根据user去重
    def __eq__(self, other):
        if isinstance(other, Message):
            return self.user == other.user
        else:
            return False

    def __ne__(self, other):
        return (not self.__eq__(other))

    def __hash__(self):
        return hash(self.user_id)

    def __str__(self):
        return self.message

    # # 判断本留言是否有回复
    # def has_child(self):
    #     return Message.objects.filter(parent=self).exists()
    #
    # # 返回本留言的所有回复
    # def get_children(self):
    #     return Message.objects.filter(parent=self)


class Notice(models.Model):
    content = models.TextField(verbose_name='注意事项')
    index = models.IntegerField(verbose_name='顺序', null=True)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '注意事项'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content
