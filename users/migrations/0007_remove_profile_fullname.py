# Generated by Django 3.0.8 on 2020-07-12 22:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20200712_1742'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='fullName',
        ),
    ]
