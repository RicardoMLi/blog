# Generated by Django 2.0 on 2019-01-05 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='博客名称')),
                ('link', models.CharField(max_length=50, verbose_name='网站链接')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '友链管理',
                'verbose_name_plural': '友链管理',
            },
        ),
    ]
