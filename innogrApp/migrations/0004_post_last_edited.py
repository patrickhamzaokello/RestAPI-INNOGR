# Generated by Django 3.0.4 on 2020-07-14 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('innogrApp', '0003_post_summary'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='last_edited',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
