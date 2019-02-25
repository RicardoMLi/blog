# Generated by Django 2.0 on 2018-12-19 01:33

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='type',
        ),
        migrations.AddField(
            model_name='blog',
            name='introduction',
            field=ckeditor_uploader.fields.RichTextUploadingField(default='', verbose_name='前言'),
        ),
        migrations.DeleteModel(
            name='BlogType',
        ),
    ]
