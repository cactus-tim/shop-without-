# Generated by Django 4.2.1 on 2023-05-23 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reg_log', '0006_alter_users_pass2'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='Face',
            new_name='FaceLink',
        ),
    ]