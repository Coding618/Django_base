# Generated by Django 2.2.5 on 2021-10-28 06:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_email_activate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='email_activate',
            new_name='email_active',
        ),
    ]
