from django.db import migrations


personal = [
    {
        'first_name': 'Петр',
        'last_name': 'Петровский',
        'middle_name': 'Владимирович',
        'energy_district': 'Сетевой район',
        'position': 'Слесарь по обслуживанию тепловых сетей',
        'rank': 2,
        'tab_number': 1010
    },
    {
        'first_name': 'Василий',
        'last_name': 'Жуков',
        'middle_name': 'Иванович',
        'energy_district': 'Сетевой район',
        'position': 'Слесарь-ремонтник',
        'rank': 5,
        'tab_number': 999
    },
    {
        'first_name': 'Григорий',
        'last_name': 'Потапов',
        'middle_name': 'Федорович',
        'energy_district': 'Сетевой район',
        'position': 'Электрогазосварщик',
        'rank': 4,
        'tab_number': 2020
    },
    {
        'first_name': 'Глеб',
        'last_name': 'Степашко',
        'middle_name': 'Андреевич',
        'energy_district': 'Сетевой район',
        'position': 'Мастер',
        'rank': None,
        'tab_number': 777
    },
]

def add_personal(apps, schema_editor):
    EnergyDistrict = apps.get_model('office', 'EnergyDistrict')
    Position = apps.get_model('office', 'Position')
    Personal = apps.get_model('office', 'Personal')
    personal_list = []
    for employee in personal:
        personal_list.append(
            Personal(
                first_name=employee['first_name'],
                last_name=employee['last_name'],
                middle_name=employee['middle_name'],
                energy_district=EnergyDistrict.objects.get(title=employee['energy_district']),
                position=Position.objects.get(name_position=employee['position']),
                rank=employee['rank'],
                tab_number=employee['tab_number']
            )
        )
    Personal.objects.bulk_create(personal_list)


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0011_add_journal'),
    ]

    operations = [
        migrations.RunPython(add_personal)
    ]
