from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from office.models import (Brigade, District, EnergyDistrict,
                           Personal, Position, PostWalking, Resolution)
from .consts import (BRGD_NUMBER, FIRST_NAME_1,
                     FIRST_NAME_2, LAST_NAME_1, LAST_NAME_2, MIDDLE_NAME_1,
                     MIDDLE_NAME_2, NAME_POSITION, PLAN_WLK,
                     POST_WLK_DETAIL_REVERSE, POST_WLK_NUMBER,
                     POST_WLK_NUMBER_2, RANK,
                     RESOLUTION_WALK, SLUG_DISTRICT,
                     TAB_NUMBER_1, TAB_NUMBER_2, TASK_WLK, TEXT_WLK,
                     TITLE_DISTRICT, TITLE_ENERGY_DISTRICT,
                     TRANSFER_WLK, USERNAME, WALK_DATE)

User = get_user_model()


class OfficeModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.energy_district = EnergyDistrict.objects.create(
            title=TITLE_ENERGY_DISTRICT,
        )
        cls.user = User.objects.create_user(
            username=USERNAME,
            energy_district=cls.energy_district
        )
        cls.district = District.objects.create(
            title=TITLE_DISTRICT,
            slug=SLUG_DISTRICT,
            master=cls.user,
            energy_district=cls.energy_district
        )
        cls.position = Position.objects.create(
            name_position=NAME_POSITION,
            walker=True,
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
        cls.post_walking = PostWalking.objects.create(
            number_post=POST_WLK_NUMBER,
            walk_date=WALK_DATE,
            district=cls.district,
            task=TASK_WLK,
            text=TEXT_WLK,
            plan=PLAN_WLK,
            fix_date=WALK_DATE,
            transfer=TRANSFER_WLK,
            author=cls.user,
        )
        cls.post_walking.members.set([cls.workman_2])
        cls.post_walking_2 = PostWalking.objects.create(
            number_post=POST_WLK_NUMBER_2,
            walk_date=WALK_DATE,
            district=cls.district,
            task=TASK_WLK,
            text=TEXT_WLK,
            plan=PLAN_WLK,
            fix_date=WALK_DATE,
            transfer=TRANSFER_WLK,
            author=cls.user,
        )
        cls.post_walking_2.members.set([cls.workman_2])
        cls.resolution = Resolution.objects.create(
            post_walking=cls.post_walking,
            author=cls.user,
            text=RESOLUTION_WALK,
        )
        cls.POST_WLK_DETAIL_URL = reverse(
            POST_WLK_DETAIL_REVERSE,
            kwargs={
                'slug_district': cls.district.slug,
                'post_id': cls.post_walking.id
            }
        )
        cls.POST_WLK_2_DETAIL_URL = reverse(
            POST_WLK_DETAIL_REVERSE,
            kwargs={
                'slug_district': cls.district.slug,
                'post_id': cls.post_walking_2.id
            }
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        energy_district = self.energy_district
        district = self.district
        position = self.position
        workman = self.workman
        brigade = self.brigade
        post_walking = self.post_walking
        personal = self.workman
        resolution = self.resolution

        object_names = {
            energy_district: energy_district.title,
            district: district.title,
            position: position.name_position,
            workman: f'{workman.last_name} {workman.first_name} {workman.middle_name}',
            brigade: f'Бригада № {brigade.number}. Мастера {brigade.master}',
            post_walking: f'{district.title}, Запись № {post_walking.pk} от {post_walking.time_create.date()}',
            personal: f'{personal.last_name} {personal.first_name} {personal.middle_name}',
            resolution: resolution.text
        }
        for field, expected_value in object_names.items():
            with self.subTest(field=field):
                self.assertEqual(
                    expected_value, str(field)
                )

    def test_get_next_post_walking(self):
        """Метод get_next_post поста обхода ссылается на следующий существующий пост в журнале обхода."""
        response = self.authorized_client.get(self.POST_WLK_DETAIL_URL)
        post = response.context.get('post')
        next_post_number = post.number_post + 1
        expected = PostWalking.objects.get(number_post=next_post_number)
        self.assertEqual(post.get_next_post(), expected)

    def test_previous_post_walking(self):
        """Метод get_previous_post поста обхода ссылается на предыдущий существующий пост в журнале обхода."""
        response = self.authorized_client.get(self.POST_WLK_2_DETAIL_URL)
        post = response.context.get('post')
        previous_post_number = post.number_post - 1
        expected = PostWalking.objects.get(number_post=previous_post_number)
        self.assertEqual(post.get_previous_post(), expected)
