# Generated by Django 2.2.5 on 2021-09-09 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0007_auto_20210909_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peopleinfo',
            name='gender',
            field=models.SmallIntegerField(choices=[(1, 'male'), (2, 'female')], default=1, verbose_name='性别'),
        ),
    ]