# Generated by Django 4.1.7 on 2023-10-18 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_customuser_energy_district'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='middle_name',
            field=models.CharField(default=123, max_length=50),
            preserve_default=False,
        ),
    ]