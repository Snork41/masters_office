# Generated by Django 4.2.6 on 2023-10-24 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0016_postwalking_is_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postwalking',
            name='walk_date',
            field=models.DateField(help_text='Введите дату в формате "ДД.ММ.ГГГГ"', verbose_name='Дата обхода'),
        ),
    ]
