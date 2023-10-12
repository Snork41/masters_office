from django.db import migrations


positions = {
    'Начальник': False,
    'Старший мастер': False,
    'Мастер': False,
    'Инженер': False,
    'Слесарь по обслуживанию тепловых сетей': True,
    'Слесарь по ремонту оборудования тепловых сетей': True,
    'Слесарь-ремонтник': True,
    'Электрогазосварщик': False,
    'Уборщик производственных помещений': False,
    'Сторож': False
}

def add_position(apps, schema_editor):
    Position = apps.get_model('office', 'Position')
    positions_list = [
        Position(name_position=name, walker=walking) for name, walking in positions.items()
    ]
    Position.objects.bulk_create(positions_list)


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0009_add_energy_district'),
    ]

    operations = [
        migrations.RunPython(add_position),
    ]
