from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import (Brigade, District, EnergyDistrict, Journal, Personal,
                      Position, PostWalking)
from .consts import (BRGD_NUMBER, DESCRIPTION_JOURNAL, FIRST_NAME_1,
                     FIRST_NAME_2, LAST_NAME_1, LAST_NAME_2, MIDDLE_NAME_1,
                     MIDDLE_NAME_2, NAME_POSITION, PLAN_WLK, POST_WLK_NUMBER,
                     RANK, RESOLUTION_WALK, SLUG_DISTRICT, SLUG_JOURNAL,
                     TAB_NUMBER_1, TAB_NUMBER_2, TASK_WLK, TEXT_WLK,
                     TITLE_DISTRICT, TITLE_ENERGY_DISTRICT, TITLE_JOURNAL,
                     TRANSFER_WLK, USERNAME, WALK_DATE)

User = get_user_model()


class OfficeModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=USERNAME)
        cls.energy_district = EnergyDistrict.objects.create(
            title=TITLE_ENERGY_DISTRICT,
        )
        cls.district = District.objects.create(
            title=TITLE_DISTRICT,
            slug=SLUG_DISTRICT,
            master=cls.user,
        )
        cls.position = Position.objects.create(
            name_position=NAME_POSITION,
        )
        cls.workman = Personal.objects.create(
            first_name=FIRST_NAME_1,
            last_name=LAST_NAME_1,
            middle_name=MIDDLE_NAME_1,
            energy_district=cls.energy_district,
            position=cls.position,
            rank=RANK,
            tab_number=TAB_NUMBER_1,
        )
        cls.workman_2 = Personal.objects.create(
            first_name=FIRST_NAME_2,
            last_name=LAST_NAME_2,
            middle_name=MIDDLE_NAME_2,
            energy_district=cls.energy_district,
            position=cls.position,
            rank=RANK,
            tab_number=TAB_NUMBER_2,
        )
        cls.brigade = Brigade.objects.create(
            number=BRGD_NUMBER,
            master=cls.user,
            brigadier=cls.workman,
        )
        cls.brigade.members.set([cls.workman_2])
        cls.journal = Journal.objects.create(
            title=TITLE_JOURNAL,
            slug=SLUG_JOURNAL,
            description=DESCRIPTION_JOURNAL,
        )
        cls.post_walking = PostWalking.objects.create(
            number_post=POST_WLK_NUMBER,
            walk_date=WALK_DATE,
            district=cls.district,
            task=TASK_WLK,
            text=TEXT_WLK,
            plan=PLAN_WLK,
            resolution=RESOLUTION_WALK,
            fix_date=WALK_DATE,
            transfer=TRANSFER_WLK,
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
