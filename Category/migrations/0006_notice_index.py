# Generated by Django 2.0 on 2018-12-21 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Category', '0005_notice'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='index',
            field=models.IntegerField(null=True, verbose_name='顺序'),
        ),
    ]
