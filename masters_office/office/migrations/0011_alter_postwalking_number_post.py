# Generated by Django 4.1.7 on 2023-03-26 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0010_remove_postwalking_journal_postwalking_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postwalking',
            name='number_post',
            field=models.PositiveIntegerField(default=1, unique=True, verbose_name='Номер записи'),
        ),
    ]
