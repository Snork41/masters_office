import json

from django.core.management.base import BaseCommand

from office.models import Personal, EnergyDistrict, Position
from masters_office.settings import BASE_DIR


class Command(BaseCommand):
    help = 'Команда для заполнения базы данных персоналом.'

    def handle(self, *args, **options):
        self.personal(self, *args)

    def personal(self, *args):
        with open(
            BASE_DIR / 'data/personal.json', 'r', encoding='utf-8'
        ) as file:
            records = []
            try:
                data = json.load(file)
                for person in data:
                    if person['rank'] == '-':
                        person['rank'] = None
                    records.append(
                        Personal(
                            first_name=person['first_name'],
                            last_name=person['last_name'],
                            middle_name=person['middle_name'],
                            energy_district=EnergyDistrict.objects.get(title=person['energy_district']),
                            position=Position.objects.get(name_position=person['position']),
                            rank=person['rank'],
                            tab_number=person['tab_number'],
                            foreman=person['foreman']
                        )
                    )
                Personal.objects.bulk_create(records)
                self.stdout.write(
                    self.style.SUCCESS(
                        'Сотрудники успешно записаны в базу данных'
                    )
                )
            except Exception as error:
                self.stdout.write(
                    self.style.ERROR(
                        f'Ошибка {error} при записи в базу данных'
                    )
                )
