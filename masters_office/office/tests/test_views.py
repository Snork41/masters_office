from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import (Brigade, District, EnergyDistrict, Journal, Personal,
                      Position, PostWalking)
from .consts import (BRGD_NUMBER, CABINET_TMPLT, CABINET_URL,
                     CREATE_POST_WLK_TMPLT, CREATE_POST_WLK_URL,
                     DESCRIPTION_JOURNAL, DISTRICTS_TMPLT, DISTRICTS_URL,
                     EDIT_POST_WLK_REVERSE, EDIT_POST_WLK_TMPLT, FIRST_NAME_1,
                     FIRST_NAME_2, INDEX_TMPLT, INDEX_URL, JOURNALS_TMPLT,
                     JOURNALS_URL, JRNL_WLK_TMPLT, JRNL_WLK_URL, LAST_NAME_1,
                     LAST_NAME_2, LOGIN_PAGE_REDIRECT, MIDDLE_NAME_1,
                     MIDDLE_NAME_2, NAME_POSITION, PLAN_WLK,
                     POST_WLK_DETAIL_REVERSE, POST_WLK_DETAIL_TMPLT,
                     POST_WLK_NUMBER, RANK, RESOLUTION_WALK, SLUG_DISTRICT,
                     SLUG_JOURNAL, TAB_NUMBER_1, TAB_NUMBER_2, TASK_WLK,
                     TEXT_WLK, TITLE_DISTRICT, TITLE_ENERGY_DISTRICT,
                     TITLE_JOURNAL, TRANSFER_WLK, UNEXISTING_PAGE, USERNAME,
                     USERNAME_AUTHOR, WALK_DATE, TITLE_DISTRICT_2, SLUG_DISTRICT_2)

User = get_user_model()


class OfficeViewsTest(TestCase):
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
        cls.district_2 = District.objects.create(
            title=TITLE_DISTRICT_2,
            slug=SLUG_DISTRICT_2,
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
        cls.post_walking_2 = PostWalking.objects.create(
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
        cls.post_walking_2.members.set([cls.workman_2])

        cls.POST_WLK_DETAIL_URL = reverse(
            POST_WLK_DETAIL_REVERSE,
            kwargs={
                'username': cls.user,
                'slug_journal': cls.journal.slug,
                'slug_district': cls.district.slug,
                'post_id': cls.post_walking.id
            }
        )
        cls.EDIT_POST_WLK_URL = reverse(
            EDIT_POST_WLK_REVERSE,
            kwargs={
                'username': cls.user,
                'slug_journal': cls.journal.slug,
                'slug_district': cls.district.slug,
                'post_id': cls.post_walking.id
            }
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_journal_page_show_correct_context(self):
        """Шаблон journals сформирован с правильным контекстом."""
        response = self.authorized_client.get(JOURNALS_URL)
        first_object = response.context.get('all_journals').first()
        self.assertEqual(first_object.title, self.journal.title)
        self.assertEqual(first_object.description, self.journal.description)
        self.assertEqual(first_object.slug, self.journal.slug)

    def test_districts_page_show_correct_context(self):
        """Шаблон districts сформирован с правильным контекстом."""
        response = self.authorized_client.get(DISTRICTS_URL)
        expected_journal = Journal.objects.get(title=self.journal)
        expected_districts = District.objects.all()
        self.assertEqual(response.context['journal'], expected_journal)
        self.assertQuerysetEqual(response.context['districts'], expected_districts, ordered=False)

    def test_journal_walk_page_show_correct_context(self):
        """Шаблон journal_walk сформирован с правильным контекстом."""
        response = self.authorized_client.get(JRNL_WLK_URL)
        excepted = PostWalking.objects.get(id=self.post_walking.id)
        self.assertEqual(response.context.get('posts').first(), excepted)

    def test_post_walking_create_page_show_correct_context(self):
        """Шаблон create_post_walking сформирован с правильным контекстом."""
        response = self.authorized_client.get(CREATE_POST_WLK_URL)
        form_fields = {
            'district': forms.fields.ChoiceField,
            'planned': forms.fields.BooleanField,
            'not_planned': forms.fields.BooleanField,
            'walk_date': forms.fields.DateTimeField,
            'members': forms.models.ModelMultipleChoiceField,
            'task': forms.fields.CharField,
            'text': forms.fields.CharField,
            'plan': forms.fields.CharField,
            'resolution': forms.fields.CharField,
            'fix_date': forms.fields.DateField,
            'transfer': forms.fields.CharField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
