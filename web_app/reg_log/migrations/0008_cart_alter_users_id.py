# Generated by Django 4.2.1 on 2023-05-23 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reg_log', '0007_rename_face_users_facelink'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('buyer_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='id')),
                ('cart', models.JSONField(verbose_name='Корзина')),
                ('status', models.BooleanField(verbose_name='Статус')),
            ],
        ),
        migrations.AlterField(
            model_name='users',
            name='ID',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='id'),
        ),
    ]
