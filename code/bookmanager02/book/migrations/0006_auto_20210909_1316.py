# Generated by Django 2.2.5 on 2021-09-09 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_auto_20210908_2347'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='peopleinfo',
            options={'verbose_name': '人物信息'},
        ),
        migrations.RenameField(
            model_name='bookinfo',
            old_name='pub_datetime',
            new_name='pub_date',
        ),
        migrations.AlterField(
            model_name='peopleinfo',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.BookInfo', verbose_name='图书'),
        ),
        migrations.AlterField(
            model_name='peopleinfo',
            name='description',
            field=models.CharField(max_length=100, null=100, verbose_name='描述信息'),
        ),
        migrations.AlterField(
            model_name='peopleinfo',
            name='gender',
            field=models.SmallIntegerField(choices=[(1, 'male'), (2, 'female')], default=1, verbose_name='性别'),
        ),
        migrations.AlterField(
            model_name='peopleinfo',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='逻辑删除'),
        ),
        migrations.AlterField(
            model_name='peopleinfo',
            name='name',
            field=models.CharField(max_length=10, unique=True, verbose_name='名称'),
        ),
    ]
