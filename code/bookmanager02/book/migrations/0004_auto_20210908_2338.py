# Generated by Django 2.2.5 on 2021-09-08 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_auto_20210908_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peopleinfo',
            name='gender',
            field=models.SmallIntegerField(choices=[(1, 'male'), (2, 'female')], default=1),
        ),
    ]
