from django.contrib.auth import get_user_model
from django.test import TestCase

from masters_office.settings import (
    BRGD_NUMBER, POST_WLK_NUM, RANK, TAB_NUMBER, WALK_DATE)

from ..models import (
    EnergyDistrict,
    District, Position,
    Personal, Brigade,
    Journal,
    PostWalking
)

User = get_user_model()


class OfficeModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.energy_district = EnergyDistrict.objects.create(
            title='Тестовый энергорайон',
        )
        cls.district = District.objects.create(
            title='Тестовый район(источник)',
            slug='Тестовый слаг',
            master=cls.user,
        )
        cls.position = Position.objects.create(
            name_position='Тестовая должность',
        )
        cls.workman = Personal.objects.create(
            first_name='Тестовое имя',
            last_name='Тестовая фаимиля',
            middle_name='Тестовое отчество',
            energy_district=cls.energy_district,
            position=cls.position,
            rank=RANK[0][1],
            tab_number=TAB_NUMBER,
        )
        cls.workman_2 = Personal.objects.create(
            first_name='Тестовое имя 2',
            last_name='Тестовая фамилия 2',
            middle_name='Тестовое отчество 2',
            energy_district=cls.energy_district,
            position=cls.position,
            rank=RANK[0][1],
            tab_number=TAB_NUMBER + 1,
        )
        cls.brigade = Brigade.objects.create(
            number=BRGD_NUMBER,
            master=cls.user,
            brigadier=cls.workman,
        )
        cls.brigade.members.set([cls.workman_2])
        cls.journal = Journal.objects.create(
            title='Тестовый журнал',
            slug='Тестовый слаг журнала',
            description='Тестовое описание',
        )
        cls.post_walking = PostWalking.objects.create(
            number_post=POST_WLK_NUM,
            walk_date=WALK_DATE,
            district=cls.district,
            task='Тестовое задание',
            text='Тестовые замечания',
            plan='Тестовые мероприятия',
            resolution='Тестовая резолюция',
            fix_date=WALK_DATE,
            transfer='Тестовый перенос ремонта',
            author=cls.user,
        )
        cls.post_walking.members.set([cls.workman_2])

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        energy_district = OfficeModelTest.energy_district
        district = OfficeModelTest.district
        position = OfficeModelTest.position
        workman = OfficeModelTest.workman
        brigade = OfficeModelTest.brigade
        journal = OfficeModelTest.journal
        post_walking = OfficeModelTest.post_walking

        object_names = {
            energy_district: energy_district.title,
            district: district.title,
            position: position.name_position,
            workman: f'{workman.last_name} {workman.first_name} {workman.middle_name}',
            brigade: f'Бригада № {brigade.number}. Мастера {brigade.master}',
            journal: journal.title,
            post_walking: f'Запись № {post_walking.pk}',
        }
        for field, expected_value in object_names.items():
            with self.subTest(field=field):
                self.assertEqual(
                    expected_value, str(field)
                )
