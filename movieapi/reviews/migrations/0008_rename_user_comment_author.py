# Generated by Django 5.0.7 on 2024-10-08 22:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_rename_author_comment_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='user',
            new_name='author',
        ),
    ]