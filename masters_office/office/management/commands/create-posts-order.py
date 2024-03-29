from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

from office.models import District, Personal, PostOrder

User = get_user_model()

class Command(BaseCommand):
    help = 'Команда для создание записей журнале учета работ по нарядам и распоряжениям.'

    def handle(self, *args, **options):
        count = options['count']
        self.posts_order(count)

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Количество создаваемых записей')

    def posts_order(self, count):
        try:
            records = []
            last_exist_post = PostOrder.objects.order_by('-number_post').first()
            district = District.objects.first()
            foreman = Personal.objects.filter(foreman=True).first()
            if last_exist_post:
                order = last_exist_post.order
                number_order = last_exist_post.number_order
            else:
                order = 'Наряд'
                number_order = 0
            increment = 1
            author=User.objects.first()
    
            for new_post in range(number_order + 1, number_order + 1 + count):
                records.append(
                    PostOrder(
                        number_post=new_post,
                        district=district,
                        order=order,
                        number_order=number_order + increment,
                        description=f'Наименование работ запись {new_post}',
                        foreman=foreman,
                        date_start_working=timezone.now(),
                        author=author
                    )
                )
                increment += 1
            PostOrder.objects.bulk_create(records)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Успешно создано {count} записей в журнале учета работ по нарядам и распоряжениям'
                )
            )
        except Exception as error:
            self.stdout.write(
                self.style.ERROR(
                    f'Ошибка {error} при записи в базу данных'
                )
            )
