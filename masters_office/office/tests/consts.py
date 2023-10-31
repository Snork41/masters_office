import datetime

from django.urls import reverse

USERNAME = 'User'
USERNAME_AUTHOR = 'authorUser'
USERNAME_BOSS = 'bossUser'
USERNAME_SECOND_ENERGY_DISCRICT = 'UserSecondEnergyDistrict'
SLUG_JOURNAL = 'test-slug-journal'
SLUG_DISTRICT = 'test-slug-district'
SLUG_DISTRICT_2 = 'test-slug-district-2'
TITLE_ENERGY_DISTRICT = 'Тестовый энергорайон'
TITLE_SECOND_ENERGY_DISTRICT = 'Тестовый энергорайон_2'
TITLE_DISTRICT = 'Тестовый район(источник)'
TITLE_DISTRICT_2 = 'Тестовый район(источник)-2'
TITLE_JOURNAL = 'Тестовый журнал'
NAME_POSITION = 'Тестовая должность'
FIRST_NAME_1 = 'Тестовое имя'
FIRST_NAME_2 = 'Тестовое имя 2'
FIRST_NAME_3_SED = 'Тестовое имя рабочего со второго энергорайона'
FIRST_NAME_4_SED = 'Тестовое имя второго рабочего со второго энергорайона'
LAST_NAME_1 = 'Тестовая фамилия'
LAST_NAME_2 = 'Тестовая фамилия 2'
LAST_NAME_3_SED = 'Тестовая фамилия рабочего со второго энергорайона'
LAST_NAME_4_SED = 'Тестовая фамилия второго рабочего со второго энергорайона'
MIDDLE_NAME_1 = 'Тестовое отчество'
MIDDLE_NAME_2 = 'Тестовое отчество 2'
MIDDLE_NAME_3_SED = 'Тестовое отчество рабочего со второго энергорайона'
MIDDLE_NAME_4_SED = 'Тестовое отчество второго рабочего со второго энергорайона'
TAB_NUMBER_1 = 1
TAB_NUMBER_2 = 2
TAB_NUMBER_3_SED = 3
TAB_NUMBER_4_SED = 4
RANK = 1
BRGD_NUMBER = 1
BRGD_SED_NUMBER = 2
DESCRIPTION_JOURNAL = 'Тестовое описание'
POST_WLK_NUMBER = 1
POST_WLK_NUMBER_2 = 2
TASK_WLK = 'Тестовое задание'
TASK_WLK_IN_EDIT_POST = 'Тестовое задание измененное'
TEXT_WLK = 'Тестовые замечания'
TEXT_WLK_2 = 'Тестовые замечания второй записи'
PLAN_WLK = 'Тестовые мероприятия'
PLAN_WLK_IN_EDIT_POST = 'Тестовые мероприятия измененные'
RESOLUTION_WALK = 'Тестовая резолюция'
RESOLUTION_WALK_2 = 'Тестовая резолюция 2'
RESOLUTION_ID = 1
TRANSFER_WLK = 'Тестовый перенос ремонта'
TRANSFER_WLK__IN_EDIT_POST = 'Тестовый перенос ремонта измененный'
WALK_DATE = datetime.date.today()
WALK_DATE_IN_EDIT_POST = datetime.date.today() - datetime.timedelta(days=1)
WALK_DATE_NOT_VALID = datetime.date.today() + datetime.timedelta(days=1)


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
ADD_RESOLUTION_REVERSE = 'office:resolution_form'
UPDATE_RESOLUTION_REVERSE = 'office:resolution_update_form'
BRIGADES_REVERSE = 'office:brigades'
EMPLOYEES_REVERSE = 'office:employees'


INDEX_URL = reverse(INDEX_REVERSE)
CABINET_URL = reverse(CABINET_REVERSE)
BRIGADES_URL = reverse(BRIGADES_REVERSE)
EMPLOYEES_URL = reverse(EMPLOYEES_REVERSE)
JOURNALS_URL = reverse(JOURNALS_REVERSE)
DISTRICTS_URL = reverse(
    DISTRICTS_REVERSE,
    kwargs={
        'slug_journal': SLUG_JOURNAL
    }
)
JRNL_WLK_URL = reverse(
    JRNL_WLK_REVERSE,
    kwargs={
        'slug_journal': SLUG_JOURNAL,
        'slug_district': SLUG_DISTRICT
    }
)
CREATE_POST_WLK_URL = reverse(
    CREATE_POST_WLK_REVERSE,
    kwargs={
        'slug_journal': SLUG_JOURNAL,
        'slug_district': SLUG_DISTRICT
    }
)
EDIT_POST_WLK_URL = reverse(
    EDIT_POST_WLK_REVERSE,
    kwargs={
        'slug_journal': SLUG_JOURNAL,
        'slug_district': SLUG_DISTRICT,
        'post_id': POST_WLK_NUMBER
    }
)
ADD_RESOLUTION_URL = reverse(
    ADD_RESOLUTION_REVERSE,
    kwargs={
        'slug_journal': SLUG_JOURNAL,
        'slug_district': SLUG_DISTRICT,
        'post_id': POST_WLK_NUMBER
    }
)
UPDATE_RESOLUTION_URL = reverse(
    UPDATE_RESOLUTION_REVERSE,
    kwargs={
        'slug_journal': SLUG_JOURNAL,
        'slug_district': SLUG_DISTRICT,
        'post_id': POST_WLK_NUMBER,
        'resolution_id': RESOLUTION_ID
    }
)


INDEX_TMPLT = 'office/index.html'
CABINET_TMPLT = 'office/cabinet.html'
JOURNALS_TMPLT = 'office/journals.html'
DISTRICTS_TMPLT = 'office/districts.html'
JRNL_WLK_TMPLT = 'office/journal_walk.html'
CREATE_POST_WLK_TMPLT = 'office/create_post_walking.html'
POST_WLK_DETAIL_TMPLT = 'office/post_walking_detail.html'
EDIT_POST_WLK_TMPLT = 'office/edit_post_walking.html'
ADD_RESOLUTION_TMPLT = 'office/includes/resolution_form.html'
UPDATE_RESOLUTION_TMPLT = 'office/includes/resolution_update_form.html'
BRIGADES_TMPL = 'office/brigades.html'
EMPLOYEES_TMPL = 'office/employees.html'
