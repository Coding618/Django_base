# Generated by Django 2.2.5 on 2021-10-25 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_activate',
            field=models.BooleanField(default=False, verbose_name='邮箱状态'),
        ),
    ]
