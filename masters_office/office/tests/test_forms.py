from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from office.models import (District, EnergyDistrict, Journal, Personal,
                           Position, PostWalking, Resolution)

from .consts import (ADD_RESOLUTION_URL, DESCRIPTION_JOURNAL, FIRST_NAME_1,
                     LAST_NAME_1, MIDDLE_NAME_1, NAME_POSITION, PLAN_WLK,
                     POST_WLK_NUMBER, RANK, RESOLUTION_WALK, RESOLUTION_WALK_2,
                     SLUG_DISTRICT, SLUG_JOURNAL, TAB_NUMBER_1, TASK_WLK,
                     TEXT_WLK, TEXT_WLK_2, TITLE_DISTRICT, TITLE_ENERGY_DISTRICT,
                     TITLE_JOURNAL, TRANSFER_WLK, UPDATE_RESOLUTION_URL,
                     USERNAME, USERNAME_BOSS, WALK_DATE, CREATE_POST_WLK_URL,
                     WALK_DATE_NOT_VALID, EDIT_POST_WLK_URL, WALK_DATE_IN_EDIT_POST,
                     TASK_WLK_IN_EDIT_POST, PLAN_WLK_IN_EDIT_POST,
                     TRANSFER_WLK__IN_EDIT_POST, FIRST_NAME_2, LAST_NAME_2,
                     MIDDLE_NAME_2, TAB_NUMBER_2)

User = get_user_model()


class PostFormTests(TestCase):
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
        cls.user_boss = User.objects.create_user(
            username=USERNAME_BOSS,
            is_staff=True,
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

    def test_create_post_walking(self):
        """Валидная форма создаёт запись обхода тепловых сетей.

        Номер записи, журнал и автор должны заполняться автоматически.
        """
        exist_posts_walking_amount = PostWalking.objects.count()
        expected_posts_walking_amount = exist_posts_walking_amount + 1
        exist_post_walking_number = self.post_walking.number_post
        expected_new_post_walking_number = exist_post_walking_number + 1
        form_data = {
            'planned': True,
            'not_planned': False,
            'walk_date': WALK_DATE,
            'task': TASK_WLK,
            'text': TEXT_WLK_2,
            'plan': PLAN_WLK,
            'fix_date': WALK_DATE,
            'transfer': TRANSFER_WLK,
            'members': self.workman.id,
            'district': self.district.id
        }
        self.authorized_client.post(CREATE_POST_WLK_URL, data=form_data)
        new_post_walking = PostWalking.objects.get(text=form_data['text'])
        self.assertEqual(PostWalking.objects.count(), expected_posts_walking_amount)
        self.assertEqual(new_post_walking.number_post, expected_new_post_walking_number)
        self.assertEqual(new_post_walking.author, self.user)
        self.assertEqual(new_post_walking.journal, self.journal)

    def test_edit_post_walking(self):
        """Валидная форма редактирует запись обхода тепловых сетей."""
        exist_post_walking = PostWalking.objects.get(author=self.user, number_post=POST_WLK_NUMBER)
        member = exist_post_walking.members.first()
        form_data = {
            'planned': not exist_post_walking.planned,
            'not_planned': not exist_post_walking.not_planned,
            'walk_date': WALK_DATE_IN_EDIT_POST,
            'task': TASK_WLK_IN_EDIT_POST,
            'text': TEXT_WLK_2,
            'plan': PLAN_WLK_IN_EDIT_POST,
            'fix_date': WALK_DATE_IN_EDIT_POST,
            'transfer': TRANSFER_WLK__IN_EDIT_POST,
            'members': self.workman_2.id,
            'district': self.district.id  # район остаётся прежним
        }
        self.authorized_client.post(EDIT_POST_WLK_URL, data=form_data)
        edit_post_walking = PostWalking.objects.get(author=self.user, number_post=POST_WLK_NUMBER)
        self.assertNotEqual(exist_post_walking.planned, edit_post_walking.planned)
        self.assertNotEqual(exist_post_walking.not_planned, edit_post_walking.not_planned)
        self.assertNotEqual(exist_post_walking.walk_date, edit_post_walking.walk_date)
        self.assertNotEqual(exist_post_walking.task, edit_post_walking.task)
        self.assertNotEqual(exist_post_walking.text, edit_post_walking.text)
        self.assertNotEqual(exist_post_walking.plan, edit_post_walking.plan)
        self.assertNotEqual(exist_post_walking.fix_date, edit_post_walking.fix_date)
        self.assertNotEqual(exist_post_walking.transfer, edit_post_walking.transfer)
        self.assertNotEqual(member, edit_post_walking.members.first())

    def test_validation_walk_date_in_new_post_walking(self):
        """Дата обхода не может быть будущей при создании записи."""
        form_data = {
            'planned': True,
            'not_planned': False,
            'walk_date': WALK_DATE_NOT_VALID,
            'task': TASK_WLK,
            'text': TEXT_WLK,
            'members': self.workman.id,
            'district': self.district.id
        }
        self.assertTrue(
            'walk_date' in self.authorized_client.post(
                CREATE_POST_WLK_URL, data=form_data
                ).context_data['form'].errors
        )

    def test_validation_select_planned_in_new_post_walking(self):
        """При создании запись обхода не может быть без типа (план/внеплан)."""
        form_data = {
            'planned': False,
            'not_planned': False,
            'walk_date': WALK_DATE,
            'task': TASK_WLK,
            'text': TEXT_WLK,
            'members': self.workman.id,
            'district': self.district.id
        }
        self.assertTrue(
            'planned' in self.authorized_client.post(
                CREATE_POST_WLK_URL, data=form_data
                ).context_data['form'].errors
        )
