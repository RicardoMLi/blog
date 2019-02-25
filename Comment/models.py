from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User

from Blog.models import Blog


class Comment(MPTTModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='用户')
    content = models.TextField(verbose_name='评论内容')
    blog = models.ForeignKey(Blog, verbose_name='博客', null=True, blank=True, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', verbose_name='父节点', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')

    class Meta:
        verbose_name = '评论管理'
        verbose_name_plural = verbose_name

    class MPTTMeta:
        parent_attr = 'parent'
        order_insertion_by = ['-created_time']

    # 根据user去重
    def __eq__(self, other):
        if isinstance(other, Comment):
            return self.user == other.user
        else:
            return False

    def __ne__(self, other):
        return (not self.__eq__(other))

    def __hash__(self):
        return hash(self.user_id)

    def __str__(self):
        return self.content

