# Generated by Django 4.0.4 on 2022-06-28 00:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PostingApp', '0006_follow'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follow',
            old_name='user_id',
            new_name='user',
        ),
    ]
