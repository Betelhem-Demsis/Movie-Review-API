# Generated by Django 5.0.7 on 2024-10-08 21:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_review_movie'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='author',
            new_name='user',
        ),
    ]
