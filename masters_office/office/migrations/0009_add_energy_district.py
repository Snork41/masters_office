from django.db import migrations


districts = [
    'Первый энергорайон',
    'Второй энергорайон',
    'Третий энергорайон',
    'Четвертый энергорайон',
    'Сетевой район'
]

def add_energy_district(apps, schema_editor):
    EnergyDistrict = apps.get_model('office', 'EnergyDistrict')
    districts_list = [EnergyDistrict(title=district) for district in districts]
    EnergyDistrict.objects.bulk_create(districts_list)


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0008_postwalking_journal_alter_resolution_post_walking'),
    ]

    operations = [
        migrations.RunPython(add_energy_district),
    ]
