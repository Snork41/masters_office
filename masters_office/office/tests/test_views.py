from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from masters_office.settings import AMOUNT_POSTS_WALK
from office.models import (Brigade, District, EnergyDistrict, Personal,
                           Position, PostOrder, PostRepairWork, PostWalking,
                           Resolution)
from .consts import (ADD_RESOLUTION_URL, ADRESS_REPAIR, ADRESS_REPAIR_2,
                     ADRESS_REPAIR_SED, BRGD_NUMBER, BRGD_SED_NUMBER,
                     BRIGADES_URL, CREATE_POST_ORDER_URL,
                     CREATE_POST_REPAIR_URL, CREATE_POST_WLK_URL,
                     DATE_END_WORKING_ORDER, DATE_END_WORKING_ORDER_2,
                     DATE_END_WORKING_ORDER_SED, DATE_END_WORKING_REPAIR,
                     DATE_END_WORKING_REPAIR_2, DATE_END_WORKING_REPAIR_SED,
                     DATE_START_WORKING_ORDER, DATE_START_WORKING_ORDER_2,
                     DATE_START_WORKING_ORDER_SED, DATE_START_WORKING_REPAIR,
                     DATE_START_WORKING_REPAIR_2,
                     DATE_START_WORKING_REPAIR_SED, DESCRIPTION_ORDER,
                     DESCRIPTION_ORDER_2, DESCRIPTION_ORDER_SED,
                     DESCRIPTION_REPAIR, DESCRIPTION_REPAIR_2,
                     DESCRIPTION_REPAIR_SED, DISTRICTS_URL,
                     EDIT_POST_REPAIR_URL, EDIT_POST_WLK_REVERSE,
                     EDIT_POST_WLK_URL, EMPLOYEES_URL, FIRST_NAME_1,
                     FIRST_NAME_2, FIRST_NAME_3_SED, FIRST_NAME_4_SED,
                     JRNL_ORDER_URL, JRNL_REPAIR_WORK_URL, JRNL_WLK_URL,
                     LAST_NAME_1, LAST_NAME_2, LAST_NAME_3_SED,
                     LAST_NAME_4_SED, MIDDLE_NAME_1, MIDDLE_NAME_2,
                     MIDDLE_NAME_3_SED, MIDDLE_NAME_4_SED, NAME_POSITION,
                     NUMBER_ORDER_ORDER, NUMBER_ORDER_ORDER_2,
                     NUMBER_ORDER_ORDER_SED, NUMBER_ORDER_REPAIR,
                     NUMBER_ORDER_REPAIR_2, NUMBER_ORDER_REPAIR_SED,
                     ORDER_ORDER, ORDER_ORDER_2, ORDER_ORDER_SED, ORDER_REPAIR,
                     ORDER_REPAIR_2, ORDER_REPAIR_SED, PLAN_WLK, PLAN_WLK_SED,
                     POST_ORDER_NUMBER, POST_ORDER_NUMBER_2,
                     POST_ORDER_NUMBER_SED, POST_REPAIR_NUMBER,
                     POST_REPAIR_NUMBER_2, POST_REPAIR_NUMBER_SED,
                     POST_WLK_DETAIL_REVERSE, POST_WLK_NUMBER,
                     POST_WLK_NUMBER_2, POST_WLK_NUMBER_SED, RANK,
                     RESOLUTION_WALK, RESOLUTION_WALK_2, SLUG_DISTRICT,
                     SLUG_DISTRICT_2, SLUG_DISTRICT_SED, TAB_NUMBER_1,
                     TAB_NUMBER_2, TAB_NUMBER_3_SED, TAB_NUMBER_4_SED,
                     TASK_WLK, TASK_WLK_SED, TEXT_WLK, TEXT_WLK_SED,
                     TITLE_DISTRICT, TITLE_DISTRICT_2, TITLE_DISTRICT_SED,
                     TITLE_ENERGY_DISTRICT, TITLE_SECOND_ENERGY_DISTRICT,
                     TRANSFER_WLK, TRANSFER_WLK_SED, UPDATE_RESOLUTION_URL,
                     USERNAME, USERNAME_AUTHOR,
                     USERNAME_SECOND_ENERGY_DISCRICT, WALK_DATE, WALK_DATE_SED)

User = get_user_model()


class OfficeViewsTest(TestCase):
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
        cls.user_author = User.objects.create_user(
            username=USERNAME_AUTHOR,
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
        cls.district_2 = District.objects.create(
            title=TITLE_DISTRICT_2,
            slug=SLUG_DISTRICT_2,
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
        cls.brigade = Brigade.objects.create(
            number=BRGD_NUMBER,
            master=cls.user,
            brigadier=cls.workman,
        )
        cls.brigade.members.set([cls.workman_2])
        cls.brigade_SED = Brigade.objects.create(
            number=BRGD_SED_NUMBER,
            master=cls.user_SED,
            brigadier=cls.workman_3_SED,
        )
        cls.brigade_SED.members.set([cls.workman_4_SED])
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
        cls.post_walking_SED = PostWalking.objects.create(
            number_post=POST_WLK_NUMBER_SED,
            walk_date=WALK_DATE_SED,
            district=cls.district_2_SED,
            task=TASK_WLK_SED,
            text=TEXT_WLK_SED,
            plan=PLAN_WLK_SED,
            fix_date=WALK_DATE_SED,
            transfer=TRANSFER_WLK_SED,
            author=cls.user_SED,
        )
        cls.post_walking_SED.members.set([cls.workman_3_SED])
        cls.resolution = Resolution.objects.create(
            post_walking=cls.post_walking,
            author=cls.user,
            text=RESOLUTION_WALK,
        )
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
        cls.post_repair_2 = PostRepairWork.objects.create(
            number_post=POST_REPAIR_NUMBER_2,
            district=cls.district_2,
            order=ORDER_REPAIR_2,
            number_order=NUMBER_ORDER_REPAIR_2,
            adress=ADRESS_REPAIR_2,
            description=DESCRIPTION_REPAIR_2,
            date_start_working=DATE_START_WORKING_REPAIR_2,
            date_end_working=DATE_END_WORKING_REPAIR_2,
            author=cls.user,
        )
        cls.post_repair_SED = PostRepairWork.objects.create(
            number_post=POST_REPAIR_NUMBER_SED,
            district=cls.district_2_SED,
            order=ORDER_REPAIR_SED,
            number_order=NUMBER_ORDER_REPAIR_SED,
            adress=ADRESS_REPAIR_SED,
            description=DESCRIPTION_REPAIR_SED,
            date_start_working=DATE_START_WORKING_REPAIR_SED,
            date_end_working=DATE_END_WORKING_REPAIR_SED,
            author=cls.user_SED,
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
        cls.post_order_2 = PostOrder.objects.create(
            number_post=POST_ORDER_NUMBER_2,
            district=cls.district_2,
            order=ORDER_ORDER_2,
            number_order=NUMBER_ORDER_ORDER_2,
            description=DESCRIPTION_ORDER_2,
            foreman=cls.workman_2,
            date_start_working=DATE_START_WORKING_ORDER_2,
            date_end_working=DATE_END_WORKING_ORDER_2,
            author=cls.user,
        )
        cls.post_order_SED = PostOrder.objects.create(
            number_post=POST_ORDER_NUMBER_SED,
            district=cls.district_2_SED,
            order=ORDER_ORDER_SED,
            number_order=NUMBER_ORDER_ORDER_SED,
            description=DESCRIPTION_ORDER_SED,
            foreman=cls.workman_3_SED,
            date_start_working=DATE_START_WORKING_ORDER_SED,
            date_end_working=DATE_END_WORKING_ORDER_SED,
            author=cls.user_SED,
        )
        cls.post_order_SED.members.set([cls.workman_4_SED])
        cls.post_order_2.members.set([cls.workman])
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
        cls.EDIT_POST_WLK_URL = reverse(
            EDIT_POST_WLK_REVERSE,
            kwargs={
                'slug_district': cls.district.slug,
                'post_id': cls.post_walking.id
            }
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.author_client = Client()
        self.author_client.force_login(self.user_author)

    def test_districts_page_show_correct_context(self):
        """Шаблон districts сформирован с правильным контекстом."""
        response = self.authorized_client.get(DISTRICTS_URL)
        expected_districts = District.objects.filter(energy_district=self.user.energy_district)
        self.assertQuerysetEqual(
            response.context['districts'], expected_districts, ordered=False
        )

    def test_journal_walk_page_show_correct_context(self):
        """Шаблон journal_walk сформирован с правильным контекстом."""
        response = self.authorized_client.get(JRNL_WLK_URL)
        excepted = PostWalking.objects.filter(district__energy_district=self.user.energy_district)
        self.assertQuerysetEqual(response.context.get('page_obj').object_list, excepted)

    def test_post_walking_create_page_show_correct_context(self):
        """Шаблон create_post_walking сформирован с правильным контекстом."""
        response = self.authorized_client.get(CREATE_POST_WLK_URL)
        form_fields = {
            'district': forms.fields.ChoiceField,
            'planned': forms.fields.BooleanField,
            'not_planned': forms.fields.BooleanField,
            'walk_date': forms.fields.DateField,
            'members': forms.models.ModelMultipleChoiceField,
            'task': forms.fields.CharField,
            'text': forms.fields.CharField,
            'plan': forms.fields.CharField,
            'fix_date': forms.fields.DateField,
            'transfer': forms.fields.CharField,
            'is_deleted': forms.BooleanField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_walking_edit_page_show_correct_context(self):
        """Шаблон edit_post_walking сформирован с правильным контекстом."""
        response = self.authorized_client.get(EDIT_POST_WLK_URL)
        form_fields = {
            'district': forms.fields.ChoiceField,
            'planned': forms.fields.BooleanField,
            'not_planned': forms.fields.BooleanField,
            'walk_date': forms.fields.DateField,
            'members': forms.models.ModelMultipleChoiceField,
            'task': forms.fields.CharField,
            'text': forms.fields.CharField,
            'plan': forms.fields.CharField,
            'fix_date': forms.fields.DateField,
            'transfer': forms.fields.CharField,
            'is_deleted': forms.BooleanField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_walking_detail_page_show_correct_context(self):
        """Шаблон post_walking_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(self.POST_WLK_DETAIL_URL)
        expected_post = PostWalking.objects.filter(
            id=self.post_walking.id).first()
        expected_district = District.objects.filter(
            id=self.district.id).first()
        self.assertEqual(response.context.get('post'), expected_post)
        self.assertEqual(response.context.get('district'), expected_district)

    def test_resolution_show_in_post(self):
        """При создании резолюции, она появляется в записи."""
        response = self.authorized_client.get(self.POST_WLK_DETAIL_URL)
        self.assertEqual(self.resolution, response.context.get('resolution'))

    def test_resolution_can_be_only_one_for_post(self):
        """Для одного поста можно создать только одну резолюцию."""
        response_1 = len(
            Resolution.objects.filter(post_walking_id=self.post_walking)
        )
        Resolution.objects.create(
            post_walking=self.post_walking,
            author=self.user_author,
            text=RESOLUTION_WALK_2
        )
        response_2 = len(
            Resolution.objects.filter(post_walking_id=self.post_walking)
        )
        self.assertEqual(response_1, response_2)

    def test_first_and_second_pages_contains_records(self):
        """Пагинация в журнале обходов."""
        PostWalking.objects.all().delete()
        posts = []
        for number in range(AMOUNT_POSTS_WALK * 2):
            posts.append(PostWalking(
                number_post=POST_WLK_NUMBER + number,
                walk_date=WALK_DATE,
                district=self.district,
                task=TASK_WLK,
                text=TEXT_WLK,
                plan=PLAN_WLK,
                fix_date=WALK_DATE,
                transfer=TRANSFER_WLK,
                author=self.user,
                )
            )
        PostWalking.objects.bulk_create(posts)
        response = self.authorized_client.get(JRNL_WLK_URL)
        self.assertEqual(
            len(response.context.get('page_obj').object_list),
            AMOUNT_POSTS_WALK
        )
        self.assertTrue(response.context.get('page_obj').has_other_pages())

    def test_resolution_form_show_correct_context(self):
        """Шаблон resolution_form сформирован с правильным контекстом."""
        response = self.authorized_client.get(ADD_RESOLUTION_URL)
        form_fields = {
            'text': forms.fields.CharField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_resolution_update_form_show_correct_context(self):
        """Шаблон resolution_update_form сформирован с правильным контекстом."""
        response = self.authorized_client.get(UPDATE_RESOLUTION_URL)
        form_fields = {
            'text': forms.fields.CharField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_brigades_page_show_correct_context(self):
        """Шаблон brigades сформирован с правильным контекстом."""
        response = self.authorized_client.get(BRIGADES_URL)
        expected_brigades = Brigade.objects.filter(
            master__energy_district=self.user.energy_district
            )
        self.assertQuerysetEqual(
            response.context['brigades'], expected_brigades
        )

    def test_employees_page_show_correct_context(self):
        """Шаблон employees сформирован с правильным контекстом."""
        response = self.authorized_client.get(EMPLOYEES_URL)
        expected_employees = Personal.objects.filter(
            energy_district=self.user.energy_district
            )
        self.assertQuerysetEqual(
            response.context['employees'], expected_employees
        )

    def test_journal_repair_work_page_show_correct_context(self):
        """Шаблон journal_repair_work сформирован с правильным контекстом."""
        response = self.authorized_client.get(JRNL_REPAIR_WORK_URL)
        excepted = PostRepairWork.objects.filter(district__energy_district=self.user.energy_district)
        self.assertQuerysetEqual(response.context.get('page_obj').object_list, excepted)

    def test_post_repair_create_page_show_correct_context(self):
        """Шаблон create_post_repair сформирован с правильным контекстом."""
        response = self.authorized_client.get(CREATE_POST_REPAIR_URL)
        form_fields = {
            'district': forms.fields.ChoiceField,
            'order': forms.fields.ChoiceField,
            'number_order': forms.fields.IntegerField,
            'adress': forms.fields.CharField,
            'description': forms.fields.CharField,
            'date_start_working': forms.fields.DateTimeField,
            'date_end_working': forms.fields.DateTimeField,
            'is_deleted': forms.fields.BooleanField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_repair_edit_page_show_correct_context(self):
        """Шаблон edit_post_repair сформирован с правильным контекстом."""
        response = self.authorized_client.get(EDIT_POST_REPAIR_URL)
        form_fields = {
            'district': forms.fields.ChoiceField,
            'order': forms.fields.ChoiceField,
            'number_order': forms.fields.IntegerField,
            'adress': forms.fields.CharField,
            'description': forms.fields.CharField,
            'date_start_working': forms.fields.DateTimeField,
            'date_end_working': forms.fields.DateTimeField,
            'is_deleted': forms.fields.BooleanField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_journal_order_page_show_correct_context(self):
        """Шаблон journal_order сформирован с правильным контекстом."""
        response = self.authorized_client.get(JRNL_ORDER_URL)
        excepted = PostOrder.objects.filter(district__energy_district=self.user.energy_district)
        self.assertQuerysetEqual(response.context.get('page_obj').object_list, excepted)

    def test_post_order_create_page_show_correct_context(self):
        """Шаблон create_post_order сформирован с правильным контекстом."""
        response = self.authorized_client.get(CREATE_POST_ORDER_URL)
        form_fields = {
            'district': forms.fields.ChoiceField,
            'order': forms.fields.ChoiceField,
            'description': forms.fields.CharField,
            'foreman': forms.ChoiceField,
            'members': forms.models.ModelMultipleChoiceField,
            'date_start_working': forms.fields.DateTimeField,
            'date_end_working': forms.fields.DateTimeField,
            'is_deleted': forms.fields.BooleanField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
