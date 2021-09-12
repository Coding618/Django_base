# Generated by Django 2.2.5 on 2021-09-08 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_auto_20210908_2338'),
    ]

    operations = [
        migrations.RenameField(
            model_name='peopleinfo',
            old_name='descriptopm',
            new_name='description',
        ),
        migrations.AlterField(
            model_name='peopleinfo',
            name='gender',
            field=models.SmallIntegerField(choices=[(2, 'female'), (1, 'male')], default=1),
        ),
    ]