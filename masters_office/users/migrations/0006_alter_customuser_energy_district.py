# Generated by Django 4.2.6 on 2023-10-29 22:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0017_alter_postwalking_walk_date'),
        ('users', '0005_alter_customuser_middle_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='energy_district',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='office.energydistrict', verbose_name='Энергорайон'),
        ),
    ]
