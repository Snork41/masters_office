import datetime

from django.urls import reverse

USERNAME = 'User'
USERNAME_AUTHOR = 'authorUser'
USERNAME_BOSS = 'bossUser'
SLUG_JOURNAL = 'test-slug-journal'
SLUG_DISTRICT = 'test-slug-district'
SLUG_DISTRICT_2 = 'test-slug-district-2'
TITLE_ENERGY_DISTRICT = 'Тестовый энергорайон'
TITLE_DISTRICT = 'Тестовый район(источник)'
TITLE_DISTRICT_2 = 'Тестовый район(источник)-2'
TITLE_JOURNAL = 'Тестовый журнал'
NAME_POSITION = 'Тестовая должность'
FIRST_NAME_1 = 'Тестовое имя'
FIRST_NAME_2 = 'Тестовое имя 2'
LAST_NAME_1 = 'Тестовая фамилия'
LAST_NAME_2 = 'Тестовая фамилия 2'
MIDDLE_NAME_1 = 'Тестовое отчество'
MIDDLE_NAME_2 = 'Тестовое отчество 2'
TAB_NUMBER_1 = 1
TAB_NUMBER_2 = 2
RANK = 1
BRGD_NUMBER = 1
DESCRIPTION_JOURNAL = 'Тестовое описание'
POST_WLK_NUMBER = 1
POST_WLK_NUMBER_2 = 1
TASK_WLK = 'Тестовое задание'
TEXT_WLK = 'Тестовые замечания'
PLAN_WLK = 'Тестовые мероприятия'
RESOLUTION_WALK = 'Тестовая резолюция'
RESOLUTION_WALK_2 = 'Тестовая резолюция 2'
TRANSFER_WLK = 'Тестовый перенос ремонта'
WALK_DATE = datetime.datetime(year=2010, month=2, day=2)


LOGIN_PAGE_REDIRECT = '/auth/login/?next='
UNEXISTING_PAGE = '/unexisting_page/'
INDEX_REVERSE = 'office:index'
CABINET_REVERSE = 'office:cabinet'
JOURNALS_REVERSE = 'office:journals'
DISTRICTS_REVERSE = 'office:districts'
JRNL_WLK_REVERSE = 'office:journal_walk'
CREATE_POST_WLK_REVERSE = 'office:create_post_walking'
POST_WLK_DETAIL_REVERSE = 'office:post_walking_detail'
EDIT_POST_WLK_REVERSE = 'office:edit_post_walking'
ADD_RESOLUTION_REVERSE = 'office:add_resolution'


INDEX_URL = reverse(INDEX_REVERSE)
CABINET_URL = reverse(CABINET_REVERSE,
                      kwargs={'username': USERNAME})
JOURNALS_URL = reverse(JOURNALS_REVERSE,
                       kwargs={'username': USERNAME})
DISTRICTS_URL = reverse(DISTRICTS_REVERSE,
                        kwargs={'username': USERNAME, 'slug_journal': SLUG_JOURNAL})
JRNL_WLK_URL = reverse(JRNL_WLK_REVERSE,
                       kwargs={'username': USERNAME, 'slug_journal': SLUG_JOURNAL, 'slug_district': SLUG_DISTRICT})
CREATE_POST_WLK_URL = reverse(CREATE_POST_WLK_REVERSE,
                              kwargs={'username': USERNAME, 'slug_journal': SLUG_JOURNAL, 'slug_district': SLUG_DISTRICT})
ADD_RESOLUTION_URL = reverse(ADD_RESOLUTION_REVERSE,
                             kwargs={'username': USERNAME, 'slug_journal': SLUG_JOURNAL, 'slug_district': SLUG_DISTRICT, 'post_id': POST_WLK_NUMBER})


INDEX_TMPLT = 'office/index.html'
CABINET_TMPLT = 'office/cabinet.html'
JOURNALS_TMPLT = 'office/journals.html'
DISTRICTS_TMPLT = 'office/districts.html'
JRNL_WLK_TMPLT = 'office/journal_walk.html'
CREATE_POST_WLK_TMPLT = 'office/create_post_walking.html'
POST_WLK_DETAIL_TMPLT = 'office/post_walking_detail.html'
EDIT_POST_WLK_TMPLT = 'office/create_post_walking.html'
RESOLUTION_TMPLT = 'office/includes/add_resolution.html'
