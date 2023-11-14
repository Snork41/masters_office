from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from office.models import (District, EnergyDistrict, Personal, Position,
                           PostOrder, PostRepairWork, PostWalking, Resolution)
from .consts import (ADD_RESOLUTION_URL, ADRESS_REPAIR, ADRESS_REPAIR_2,
                     CREATE_POST_ORDER_URL, CREATE_POST_REPAIR_URL,
                     CREATE_POST_WLK_URL, DATE_END_WORKING_ORDER,
                     DATE_END_WORKING_ORDER_2,
                     DATE_END_WORKING_ORDER_NOT_VALID, DATE_END_WORKING_REPAIR,
                     DATE_END_WORKING_REPAIR_2,
                     DATE_END_WORKING_REPAIR_NOT_VALID,
                     DATE_START_WORKING_ORDER, DATE_START_WORKING_ORDER_2,
                     DATE_START_WORKING_REPAIR, DATE_START_WORKING_REPAIR_2,
                     DESCRIPTION_ORDER, DESCRIPTION_ORDER_2,
                     DESCRIPTION_REPAIR, DESCRIPTION_REPAIR_2,
                     EDIT_POST_REPAIR_URL, EDIT_POST_WLK_URL, FIRST_NAME_1,
                     FIRST_NAME_2, FIRST_NAME_3_SED, FIRST_NAME_4_SED,
                     LAST_NAME_1, LAST_NAME_2, LAST_NAME_3_SED,
                     LAST_NAME_4_SED, MIDDLE_NAME_1, MIDDLE_NAME_2,
                     MIDDLE_NAME_3_SED, MIDDLE_NAME_4_SED, NAME_POSITION,
                     NUMBER_ORDER_ORDER, NUMBER_ORDER_REPAIR,
                     NUMBER_ORDER_REPAIR_2, ORDER_ORDER, ORDER_ORDER_2,
                     ORDER_REPAIR, ORDER_REPAIR_2, PLAN_WLK,
                     PLAN_WLK_IN_EDIT_POST, POST_ORDER_NUMBER,
                     POST_REPAIR_NUMBER, POST_WLK_NUMBER, RANK,
                     RESOLUTION_WALK, RESOLUTION_WALK_2, SLUG_DISTRICT,
                     SLUG_DISTRICT_SED, TAB_NUMBER_1, TAB_NUMBER_2,
                     TAB_NUMBER_3_SED, TAB_NUMBER_4_SED, TASK_WLK,
                     TASK_WLK_IN_EDIT_POST, TEXT_WLK, TEXT_WLK_2,
                     TITLE_DISTRICT, TITLE_DISTRICT_SED, TITLE_ENERGY_DISTRICT,
                     TITLE_SECOND_ENERGY_DISTRICT, TRANSFER_WLK,
                     TRANSFER_WLK__IN_EDIT_POST, UPDATE_RESOLUTION_URL,
                     USERNAME, USERNAME_BOSS, USERNAME_SECOND_ENERGY_DISCRICT,
                     WALK_DATE, WALK_DATE_IN_EDIT_POST, WALK_DATE_NOT_VALID,
                     EDIT_POST_ORDER_URL)

User = get_user_model()


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.energy_district = EnergyDistrict.objects.create(
            title=TITLE_ENERGY_DISTRICT,
        )
        cls.energy_district_2 = EnergyDistrict.objects.create(
            title=TITLE_SECOND_ENERGY_DISTRICT,
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
        cls.user_SED = User.objects.create_user(
            username=USERNAME_SECOND_ENERGY_DISCRICT,
            energy_district=cls.energy_district_2
        )
        cls.district = District.objects.create(
            title=TITLE_DISTRICT,
            slug=SLUG_DISTRICT,
            master=cls.user,
            energy_district=cls.energy_district
        )
        cls.district_2_SED = District.objects.create(
            title=TITLE_DISTRICT_SED,
            slug=SLUG_DISTRICT_SED,
            master=cls.user_SED,
            energy_district=cls.energy_district_2
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
        cls.workman_3_SED = Personal.objects.create(
            first_name=FIRST_NAME_3_SED,
            last_name=LAST_NAME_3_SED,
            middle_name=MIDDLE_NAME_3_SED,
            energy_district=cls.energy_district_2,
            position=cls.position,
            rank=RANK,
            tab_number=TAB_NUMBER_3_SED,
        )
        cls.workman_4_SED = Personal.objects.create(
            first_name=FIRST_NAME_4_SED,
            last_name=LAST_NAME_4_SED,
            middle_name=MIDDLE_NAME_4_SED,
            energy_district=cls.energy_district_2,
            position=cls.position,
            rank=RANK,
            tab_number=TAB_NUMBER_4_SED,
        )
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
        cls.post_walking.members.set([cls.workman])
        cls.post_repair = PostRepairWork.objects.create(
            number_post=POST_REPAIR_NUMBER,
            district=cls.district,
            order=ORDER_REPAIR,
            number_order=NUMBER_ORDER_REPAIR,
            adress=ADRESS_REPAIR,
            description=DESCRIPTION_REPAIR,
            date_start_working=DATE_START_WORKING_REPAIR,
            date_end_working=DATE_END_WORKING_REPAIR,
            author=cls.user,
        )
        cls.post_order = PostOrder.objects.create(
            number_post=POST_ORDER_NUMBER,
            district=cls.district,
            order=ORDER_ORDER,
            number_order=NUMBER_ORDER_ORDER,
            description=DESCRIPTION_ORDER,
            foreman=cls.workman,
            date_start_working=DATE_START_WORKING_ORDER,
            date_end_working=DATE_END_WORKING_ORDER,
            author=cls.user,
        )
        cls.post_order.members.set([cls.workman_2])

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

        Номер записи и автор должны заполняться автоматически.
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
        response = self.authorized_client.post(CREATE_POST_WLK_URL, data=form_data)
        self.assertFalse(response.context['form'].is_valid())
        self.assertTrue('walk_date' in response.context_data['form'].errors)

    def test_validation_walk_date_in_edit_post_walking(self):
        """Дата обхода не может быть будущей при редактировании записи."""
        form_data = {
            'planned': True,
            'not_planned': False,
            'walk_date': WALK_DATE_NOT_VALID,
            'task': TASK_WLK,
            'text': TEXT_WLK,
            'members': self.workman.id,
            'district': self.district.id
        }
        response = self.authorized_client.post(EDIT_POST_WLK_URL, data=form_data)
        self.assertFalse(response.context['form'].is_valid())
        self.assertTrue('walk_date' in response.context_data['form'].errors)

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
        response = self.authorized_client.post(CREATE_POST_WLK_URL, data=form_data)
        self.assertFalse(response.context['form'].is_valid())
        self.assertTrue('planned' in response.context_data['form'].errors)

    def test_validation_select_planned_in_edit_post_walking(self):
        """При редактировании запись обхода не может быть без типа (план/внеплан)."""
        form_data = {
            'planned': False,
            'not_planned': False,
            'walk_date': WALK_DATE,
            'task': TASK_WLK,
            'text': TEXT_WLK,
            'members': self.workman.id,
            'district': self.district.id
        }
        response = self.authorized_client.post(EDIT_POST_WLK_URL, data=form_data)
        self.assertFalse(response.context['form'].is_valid())
        self.assertTrue('planned' in response.context_data['form'].errors)

    def test_validation_select_members_in_new_post_walking(self):
        """При создании записи обхода члены бригады не могут быть с другого энергорайона."""
        form_data = {
            'planned': True,
            'not_planned': False,
            'walk_date': WALK_DATE,
            'task': TASK_WLK,
            'text': TEXT_WLK_2,
            'members': self.workman_3_SED.id,
            'district': self.district.id
        }
        response = self.authorized_client.post(CREATE_POST_WLK_URL, data=form_data)
        self.assertFalse(response.context['form'].is_valid())
        self.assertTrue('members' in response.context_data['form'].errors)

    def test_validation_select_members_in_edit_post_walking(self):
        """При редактировании записи обхода члены бригады не могут быть с другого энергорайона."""
        form_data = {
            'planned': True,
            'not_planned': False,
            'walk_date': WALK_DATE,
            'task': TASK_WLK,
            'text': TEXT_WLK_2,
            'members': self.workman_3_SED.id,
            'district': self.district.id
        }
        response = self.authorized_client.post(EDIT_POST_WLK_URL, data=form_data)
        self.assertFalse(response.context['form'].is_valid())
        self.assertTrue('members' in response.context_data['form'].errors)

    def test_validation_select_district_in_new_post_walking(self):
        """При создании записи обхода источник (район) не может быть другого энергорайона."""
        form_data = {
            'planned': True,
            'not_planned': False,
            'walk_date': WALK_DATE,
            'task': TASK_WLK,
            'text': TEXT_WLK_2,
            'members': self.workman.id,
            'district': self.district_2_SED.id
        }
        response = self.authorized_client.post(CREATE_POST_WLK_URL, data=form_data)
        self.assertFalse(response.context['form'].is_valid())
        self.assertTrue('district' in response.context_data['form'].errors)

    def test_create_post_repair_work(self):
        """Валидная форма создаёт запись в журнале ремонтных работ.

        Номер записи и автор должны заполняться автоматически.
        """
        exist_posts_repair_amount = PostRepairWork.objects.count()
        expected_posts_repair_amount = exist_posts_repair_amount + 1
        exist_post_repair_number = self.post_repair.number_post
        expected_new_post_repair_number = exist_post_repair_number + 1
        form_data = {
            'district': self.district.id,
            'order': ORDER_REPAIR,
            'number_order': NUMBER_ORDER_REPAIR,
            'adress': ADRESS_REPAIR,
            'description': DESCRIPTION_REPAIR_2,
            'date_start_working': DATE_START_WORKING_REPAIR,
            'date_end_working': DATE_END_WORKING_REPAIR,
        }
        self.authorized_client.post(CREATE_POST_REPAIR_URL, data=form_data)
        new_post_repair = PostRepairWork.objects.get(description=form_data['description'])
        self.assertEqual(PostRepairWork.objects.count(), expected_posts_repair_amount)
        self.assertEqual(new_post_repair.number_post, expected_new_post_repair_number)
        self.assertEqual(new_post_repair.author, self.user)

    def test_edit_post_repair_work(self):
        """Валидная форма редактирует запись в журнале ремонтных работ."""
        exist_post_repair = PostRepairWork.objects.get(author=self.user, number_post=POST_REPAIR_NUMBER)
        form_data = {
            'district': self.district.id,  # район не меняется
            'order': ORDER_REPAIR_2,
            'number_order': NUMBER_ORDER_REPAIR_2,
            'adress': ADRESS_REPAIR_2,
            'description': DESCRIPTION_REPAIR_2,
            'date_start_working': DATE_START_WORKING_REPAIR_2,
            'date_end_working': DATE_END_WORKING_REPAIR_2,
        }
        self.authorized_client.post(EDIT_POST_REPAIR_URL, data=form_data)
        edit_post_repair = PostRepairWork.objects.get(author=self.user, number_post=POST_REPAIR_NUMBER)
        self.assertNotEqual(exist_post_repair.order, edit_post_repair.order)
        self.assertNotEqual(exist_post_repair.number_order, edit_post_repair.number_order)
        self.assertNotEqual(exist_post_repair.adress, edit_post_repair.adress)
        self.assertNotEqual(exist_post_repair.description, edit_post_repair.description)
        self.assertNotEqual(exist_post_repair.date_start_working, edit_post_repair.date_start_working)
        self.assertNotEqual(exist_post_repair.date_end_working, edit_post_repair.date_end_working)

    def test_validation_date_end_working_in_new_post_repair(self):
        """
        При создании записи в журнале ремонтных работ,
        дата окончания работ не может быть раньше даты начала работ.
        """
        form_data = {
            'district': self.district.id,
            'order': ORDER_REPAIR,
            'number_order': NUMBER_ORDER_REPAIR,
            'adress': ADRESS_REPAIR,
            'description': DESCRIPTION_REPAIR_2,
            'date_start_working': DATE_START_WORKING_REPAIR,
            'date_end_working': DATE_END_WORKING_REPAIR_NOT_VALID,
        }
        response = self.authorized_client.post(CREATE_POST_REPAIR_URL, data=form_data)
        self.assertFalse(response.context['form'].is_valid())
        self.assertTrue('date_end_working' in response.context_data['form'].errors)

    def test_create_post_order(self):
        """Валидная форма создаёт запись в журнале учета работ по нарядам и распоряжениям.

        Номер записи, номер наряда/распоряжения и автор должны заполняться автоматически.
        """
        exist_posts_order_amount = PostOrder.objects.count()
        expected_posts_order_amount = exist_posts_order_amount + 1
        exist_post_order_number = self.post_order.number_post
        expected_new_post_order_number = exist_post_order_number + 1
        exist_post_order_number_order = self.post_order.number_order
        expected_new_post_order_number_order = exist_post_order_number_order + 1

        form_data = {
            'district': self.district.id,
            'order': ORDER_ORDER,
            'description': DESCRIPTION_ORDER_2,
            'foreman': self.workman_2.id,
            'members': self.workman.id,
            'date_start_working': DATE_START_WORKING_ORDER_2,
            'date_end_working': DATE_END_WORKING_ORDER_2,
        }
        self.authorized_client.post(CREATE_POST_ORDER_URL, data=form_data)
        new_post_order = PostOrder.objects.get(description=form_data['description'])
        self.assertEqual(PostOrder.objects.count(), expected_posts_order_amount)
        self.assertEqual(new_post_order.number_post, expected_new_post_order_number)
        self.assertEqual(new_post_order.number_order, expected_new_post_order_number_order)
        self.assertEqual(new_post_order.author, self.user)

    def test_validation_date_end_working_in_new_post_order(self):
        """
        При создании записи в журнале учета нарядов и распоряжений
        дата окончания работ не может быть раньше даты начала работ.
        """
        form_data = {
            'district': self.district.id,
            'order': ORDER_ORDER,
            'description': DESCRIPTION_ORDER_2,
            'foreman': self.workman_2.id,
            'members': self.workman.id,
            'date_start_working': DATE_START_WORKING_ORDER,
            'date_end_working': DATE_END_WORKING_ORDER_NOT_VALID,
        }
        response = self.authorized_client.post(CREATE_POST_ORDER_URL, data=form_data)
        self.assertFalse(response.context['form'].is_valid())
        self.assertTrue('date_end_working' in response.context_data['form'].errors)

    def test_edit_post_order(self):
        """Валидная форма редактирует запись в журнале учета нарядов и распоряжений."""
        exist_post_order = PostOrder.objects.get(author=self.user, number_post=POST_ORDER_NUMBER)
        member = exist_post_order.members.first()
        form_data = {
            'district': self.district.id,
            'order': ORDER_ORDER_2,
            'description': DESCRIPTION_ORDER_2,
            'foreman': self.workman_2.id,
            'members': self.workman.id,
            'date_start_working': DATE_START_WORKING_ORDER_2,
            'date_end_working': DATE_END_WORKING_ORDER_2,
        }
        self.authorized_client.post(EDIT_POST_ORDER_URL, data=form_data)
        edit_post_order = PostOrder.objects.get(author=self.user, number_post=POST_ORDER_NUMBER)
        self.assertNotEqual(exist_post_order.order, edit_post_order.order)
        self.assertNotEqual(exist_post_order.description, edit_post_order.description)
        self.assertNotEqual(exist_post_order.foreman, edit_post_order.foreman)
        self.assertNotEqual(member, edit_post_order.members.first())
        self.assertNotEqual(exist_post_order.date_start_working, edit_post_order.date_start_working)
        self.assertNotEqual(exist_post_order.date_end_working, edit_post_order.date_end_working)
        self.assertEqual(exist_post_order.number_order, edit_post_order.number_order)

    # def test_validation_district_in_edit_post_walking(self):
    #     """При редактировании записи обхода источник (район) нельзя изменить."""
