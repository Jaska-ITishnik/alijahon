# Generated by Django 5.1.1 on 2024-09-09 08:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0003_remove_stream_slug_stream_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='slug',
        ),
    ]
