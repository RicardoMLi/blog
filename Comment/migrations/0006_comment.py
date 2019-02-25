# Generated by Django 2.0 on 2018-12-25 08:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Blog', '0012_auto_20181225_1039'),
        ('Comment', '0005_auto_20181225_1531'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='评论内容')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='评论时间')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('blog', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Blog.Blog', verbose_name='博客')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='Comment.Comment', verbose_name='父节点')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '评论管理',
                'verbose_name_plural': '评论管理',
            },
        ),
    ]
