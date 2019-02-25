# Generated by Django 2.0 on 2018-12-25 02:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0009_blog_like_num'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='标签')),
            ],
            options={
                'verbose_name': '标签管理',
                'verbose_name_plural': '标签管理',
            },
        ),
        migrations.AddField(
            model_name='blog',
            name='tag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Blog.Tag', verbose_name='标签'),
        ),
    ]
