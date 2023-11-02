from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from office.models import (Brigade, District, EnergyDistrict, Journal,
                           Personal, Position, PostWalking)
from .consts import (BRGD_NUMBER, CABINET_TMPLT, CABINET_URL,
                     CREATE_POST_WLK_TMPLT, CREATE_POST_WLK_URL,
                     DESCRIPTION_JOURNAL, DISTRICTS_TMPLT, DISTRICTS_URL,
                     EDIT_POST_WLK_REVERSE, EDIT_POST_WLK_TMPLT, FIRST_NAME_1,
                     FIRST_NAME_2, INDEX_TMPLT, INDEX_URL, JOURNALS_TMPLT,
                     JOURNALS_URL, JRNL_WLK_TMPLT, JRNL_WLK_URL, LAST_NAME_1,
                     LAST_NAME_2, LOGIN_PAGE_REDIRECT, MIDDLE_NAME_1,
                     MIDDLE_NAME_2, NAME_POSITION, PLAN_WLK,
                     POST_WLK_DETAIL_REVERSE, POST_WLK_DETAIL_TMPLT,
                     POST_WLK_NUMBER, RANK, SLUG_DISTRICT, SLUG_JOURNAL,
                     TAB_NUMBER_1, TAB_NUMBER_2, TASK_WLK, TEXT_WLK,
                     TITLE_DISTRICT, TITLE_ENERGY_DISTRICT, TITLE_JOURNAL,
                     TRANSFER_WLK, UNEXISTING_PAGE, USERNAME, USERNAME_AUTHOR,
                     WALK_DATE, BRIGADES_URL, BRIGADES_TMPL, EMPLOYEES_URL,
                     EMPLOYEES_TMPL)

User = get_user_model()


class OfficeURLTest(TestCase):
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
        cls.user_author = User.objects.create_user(
            username=USERNAME_AUTHOR,
            energy_district=cls.energy_district
        )
        cls.district = District.objects.create(
            title=TITLE_DISTRICT,
            slug=SLUG_DISTRICT,
            master=cls.user_author,
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
            master=cls.user_author,
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
            journal=cls.journal,
            district=cls.district,
            task=TASK_WLK,
            text=TEXT_WLK,
            plan=PLAN_WLK,
            fix_date=WALK_DATE,
            transfer=TRANSFER_WLK,
            author=cls.user_author,
        )
        cls.post_walking.members.set([cls.workman_2])

        cls.POST_WLK_DETAIL_URL = reverse(
            POST_WLK_DETAIL_REVERSE,
            kwargs={
                'slug_journal': cls.journal.slug,
                'slug_district': cls.district.slug,
                'post_id': cls.post_walking.id
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

    def test_urls_access_for_anonymous(self):
        """Доступ страниц для анонимного пользователя"""
        url = {
            INDEX_URL: HTTPStatus.OK,
            UNEXISTING_PAGE: HTTPStatus.NOT_FOUND,
        }
        for url_name, expected_code in url.items():
            with self.subTest(url_name=url_name):
                self.assertEqual(
                    self.client.get(url_name).status_code, expected_code
                )

    def test_urls_access_for_authorized_client(self):
        """Доступ страниц для авторизованного пользователя-не автора"""
        url = {
            UNEXISTING_PAGE: HTTPStatus.NOT_FOUND,
            INDEX_URL: HTTPStatus.OK,
            CABINET_URL: HTTPStatus.OK,
            JOURNALS_URL: HTTPStatus.OK,
            DISTRICTS_URL: HTTPStatus.OK,
            JRNL_WLK_URL: HTTPStatus.OK,
            CREATE_POST_WLK_URL: HTTPStatus.OK,
            self.POST_WLK_DETAIL_URL: HTTPStatus.OK,
            self.EDIT_POST_WLK_URL: HTTPStatus.FOUND,
            BRIGADES_URL: HTTPStatus.OK,
            EMPLOYEES_URL: HTTPStatus.OK,
        }
        for url_name, expected_code in url.items():
            with self.subTest(url_name=url_name):
                if expected_code == HTTPStatus.FOUND:
                    self.assertRedirects(
                        self.authorized_client.get(url_name, follow=True),
                        self.POST_WLK_DETAIL_URL
                    )
                else:
                    self.assertEqual(
                        self.authorized_client.get(url_name).status_code,
                        expected_code)

    def test_urls_access_for_author_client(self):
        """Доступ страниц для пользователя-автора"""
        url = {
            UNEXISTING_PAGE: HTTPStatus.NOT_FOUND,
            INDEX_URL: HTTPStatus.OK,
            CABINET_URL: HTTPStatus.OK,
            JOURNALS_URL: HTTPStatus.OK,
            DISTRICTS_URL: HTTPStatus.OK,
            JRNL_WLK_URL: HTTPStatus.OK,
            CREATE_POST_WLK_URL: HTTPStatus.OK,
            self.POST_WLK_DETAIL_URL: HTTPStatus.OK,
            self.EDIT_POST_WLK_URL: HTTPStatus.OK,
            BRIGADES_URL: HTTPStatus.OK,
            EMPLOYEES_URL: HTTPStatus.OK,
        }
        for url_name, expected_code in url.items():
            with self.subTest(url_name=url_name):
                self.assertEqual(
                    self.author_client.get(url_name).status_code,
                    expected_code)

    def test_urls_redirect_anonymous_to_login(self):
        """Страница по любому адресу, кроме index, перенаправит
        анонимного пользователя на страницу логина
        """
        urls = [
            CABINET_URL,
            JOURNALS_URL,
            DISTRICTS_URL,
            JRNL_WLK_URL,
            CREATE_POST_WLK_URL,
            self.POST_WLK_DETAIL_URL,
            self.EDIT_POST_WLK_URL,
            BRIGADES_URL,
            EMPLOYEES_URL,
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                if 'edit_post_walking' in url:
                    url = self.POST_WLK_DETAIL_URL
                self.assertRedirects(response, LOGIN_PAGE_REDIRECT + url)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            INDEX_URL: INDEX_TMPLT,
            CABINET_URL: CABINET_TMPLT,
            JOURNALS_URL: JOURNALS_TMPLT,
            DISTRICTS_URL: DISTRICTS_TMPLT,
            JRNL_WLK_URL: JRNL_WLK_TMPLT,
            CREATE_POST_WLK_URL: CREATE_POST_WLK_TMPLT,
            self.POST_WLK_DETAIL_URL: POST_WLK_DETAIL_TMPLT,
            self.EDIT_POST_WLK_URL: EDIT_POST_WLK_TMPLT,
            BRIGADES_URL: BRIGADES_TMPL,
            EMPLOYEES_URL: EMPLOYEES_TMPL,
        }
        for address, template in templates_url_names.items():
            with self.subTest(template=template):
                response = self.author_client.get(address)
                self.assertTemplateUsed(response, template)
