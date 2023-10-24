from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from masters_office.settings import AMOUNT_POSTS_WALK
from office.models import (Brigade, District, EnergyDistrict, Journal,
                           Personal, Position, PostWalking, Resolution)
from .consts import (BRGD_NUMBER, CREATE_POST_WLK_URL, DESCRIPTION_JOURNAL,
                     DISTRICTS_URL, EDIT_POST_WLK_REVERSE, FIRST_NAME_1,
                     FIRST_NAME_2, JOURNALS_URL, JRNL_WLK_URL, LAST_NAME_1,
                     LAST_NAME_2, MIDDLE_NAME_1, MIDDLE_NAME_2, NAME_POSITION,
                     PLAN_WLK, POST_WLK_DETAIL_REVERSE, POST_WLK_NUMBER,
                     POST_WLK_NUMBER_2, RANK, RESOLUTION_WALK,
                     RESOLUTION_WALK_2, SLUG_DISTRICT, SLUG_DISTRICT_2,
                     SLUG_JOURNAL, TAB_NUMBER_1, TAB_NUMBER_2, TASK_WLK,
                     TEXT_WLK, TITLE_DISTRICT, TITLE_DISTRICT_2,
                     TITLE_ENERGY_DISTRICT, TITLE_JOURNAL, TRANSFER_WLK,
                     USERNAME, USERNAME_AUTHOR, WALK_DATE, ADD_RESOLUTION_URL,
                     UPDATE_RESOLUTION_URL, BRIGADES_URL, TITLE_SECOND_ENERGY_DISTRICT,
                     USERNAME_SECOND_ENERGY_DISCRICT,
                     FIRST_NAME_3_SED, FIRST_NAME_4_SED, LAST_NAME_3_SED,
                     LAST_NAME_4_SED, MIDDLE_NAME_3_SED, MIDDLE_NAME_4_SED,
                     BRGD_SED_NUMBER, TAB_NUMBER_3_SED, TAB_NUMBER_4_SED,
                     EMPLOYEES_URL)

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
        )
        cls.district_2 = District.objects.create(
            title=TITLE_DISTRICT_2,
            slug=SLUG_DISTRICT_2,
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
        cls.post_walking.members.set([cls.workman_2])
        cls.post_walking_2 = PostWalking.objects.create(
            number_post=POST_WLK_NUMBER_2,
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
        cls.post_walking_2.members.set([cls.workman_2])
        cls.resolution = Resolution.objects.create(
            post_walking=cls.post_walking,
            author=cls.user,
            text=RESOLUTION_WALK,
        )
        cls.POST_WLK_DETAIL_URL = reverse(
            POST_WLK_DETAIL_REVERSE,
            kwargs={
                'slug_journal': cls.journal.slug,
                'slug_district': cls.district.slug,
                'post_id': cls.post_walking.id
            }
        )
        cls.POST_WLK_2_DETAIL_URL = reverse(
            POST_WLK_DETAIL_REVERSE,
            kwargs={
                'slug_journal': cls.journal.slug,
                'slug_district': cls.district.slug,
                'post_id': cls.post_walking_2.id
            }
        )
        cls.EDIT_POST_WLK_URL = reverse(
            EDIT_POST_WLK_REVERSE,
            kwargs={
                'slug_journal': cls.journal.slug,
                'slug_district': cls.district.slug,
                'post_id': cls.post_walking.id
            }
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.author_client = Client()
        self.author_client.force_login(self.user_author)

    def test_journals_page_show_correct_context(self):
        """Шаблон journals сформирован с правильным контекстом."""
        response = self.authorized_client.get(JOURNALS_URL)
        last_object = response.context.get('all_journals').last()
        self.assertEqual(last_object.title, self.journal.title)
        self.assertEqual(last_object.description, self.journal.description)
        self.assertEqual(last_object.slug, self.journal.slug)

    def test_districts_page_show_correct_context(self):
        """Шаблон districts сформирован с правильным контекстом."""
        response = self.authorized_client.get(DISTRICTS_URL)
        expected_journal = Journal.objects.get(title=self.journal)
        expected_districts = District.objects.all()
        self.assertEqual(response.context['journal'], expected_journal)
        self.assertQuerysetEqual(
            response.context['districts'], expected_districts, ordered=False
        )

    def test_journal_walk_page_show_correct_context(self):
        """Шаблон journal_walk сформирован с правильным контекстом."""
        response = self.authorized_client.get(JRNL_WLK_URL)
        excepted = PostWalking.objects.filter()
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
        expected_journal = Journal.objects.filter(
            id=self.journal.id).first()
        self.assertEqual(response.context.get('post'), expected_post)
        self.assertEqual(response.context.get('district'), expected_district)
        self.assertEqual(response.context.get('journal'), expected_journal)

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
                journal=self.journal,
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
