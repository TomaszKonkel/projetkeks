# Generated by Django 3.1.13 on 2022-01-21 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='visible',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
