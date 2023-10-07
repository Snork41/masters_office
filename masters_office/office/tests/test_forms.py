from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from office.models import (District, EnergyDistrict, Journal, Personal,
                           Position, PostWalking, Resolution)

from .consts import (ADD_RESOLUTION_URL, DESCRIPTION_JOURNAL, FIRST_NAME_1,
                     LAST_NAME_1, MIDDLE_NAME_1, NAME_POSITION, PLAN_WLK,
                     POST_WLK_NUMBER, RANK, RESOLUTION_WALK,
                     RESOLUTION_WALK_2, SLUG_DISTRICT,
                     SLUG_JOURNAL, TAB_NUMBER_1, TASK_WLK, TEXT_WLK,
                     TITLE_DISTRICT, TITLE_ENERGY_DISTRICT, TITLE_JOURNAL,
                     TRANSFER_WLK, USERNAME, USERNAME_BOSS, WALK_DATE,
                     UPDATE_RESOLUTION_URL)

User = get_user_model()


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=USERNAME)
        cls.user_boss = User.objects.create_user(
            username=USERNAME_BOSS, is_staff=True
        )
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
        cls.journal = Journal.objects.create(
            title=TITLE_JOURNAL,
            slug=SLUG_JOURNAL,
            description=DESCRIPTION_JOURNAL,
        )
        cls.post_walking = PostWalking.objects.create(
            number_post=POST_WLK_NUMBER,
            walk_date=WALK_DATE,
            journal=cls.journal,
            district=cls.district,
            task=TASK_WLK,
            text=TEXT_WLK,
            plan=PLAN_WLK,
            fix_date=WALK_DATE,
            transfer=TRANSFER_WLK,
            author=cls.user,
        )
        cls.post_walking.members.set([cls.workman])

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.boss_client = Client()
        self.boss_client.force_login(self.user_boss)

    def test_create_resolution(self):
        """Валидная форма создаёт резолюцию."""
        form_data = {'text': RESOLUTION_WALK}
        self.boss_client.post(ADD_RESOLUTION_URL, data=form_data)
        self.assertTrue(
            Resolution.objects.filter(text=form_data['text']).exists())
        
    def test_update_resolution(self):
        """Валидная форма редактирует резолюцию."""
        form_data = {'text': RESOLUTION_WALK}
        self.boss_client.post(ADD_RESOLUTION_URL, data=form_data)
        resolution_before = Resolution.objects.all().first()
        form_data = {'text': RESOLUTION_WALK_2}
        self.boss_client.post(UPDATE_RESOLUTION_URL, data=form_data)
        resolution_after = Resolution.objects.all().first()
        self.assertEqual(resolution_before.id, resolution_after.id)
        self.assertNotEqual(resolution_before.text, resolution_after.text)

    def test_only_boss_can_make_create_resolution(self):
        """Только Начальник может оставлять резолюцию."""
        form_data = {'text': RESOLUTION_WALK}
        self.authorized_client.post(ADD_RESOLUTION_URL, data=form_data)
        self.assertFalse(
            Resolution.objects.filter(text=form_data['text']).exists())
