# Generated by Django 4.2.6 on 2023-10-24 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_customuser_middle_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='middle_name',
            field=models.CharField(max_length=50, verbose_name='Отчество'),
        ),
    ]
