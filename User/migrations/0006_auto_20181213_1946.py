# Generated by Django 2.0 on 2018-12-13 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0005_quote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='user',
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
