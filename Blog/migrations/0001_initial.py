# Generated by Django 2.0 on 2018-12-12 14:14

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='内容')),
                ('created_time', models.DateField(auto_now_add=True, verbose_name='日期')),
                ('image', models.ImageField(upload_to='blog/', verbose_name='博客图片')),
            ],
            options={
                'verbose_name': '博客',
                'verbose_name_plural': '博客',
            },
        ),
        migrations.CreateModel(
            name='BlogType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20, verbose_name='类型')),
            ],
            options={
                'verbose_name': '博客类型',
                'verbose_name_plural': '博客类型',
            },
        ),
        migrations.AddField(
            model_name='blog',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Blog.BlogType', verbose_name='类型'),
        ),
    ]
