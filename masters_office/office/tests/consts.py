import datetime

from django.urls import reverse


USERNAME = 'User'
USERNAME_AUTHOR = 'authorUser'
USERNAME_BOSS = 'bossUser'
USERNAME_SECOND_ENERGY_DISCRICT = 'UserSecondEnergyDistrict'

SLUG_DISTRICT = 'test-slug-district'
SLUG_DISTRICT_2 = 'test-slug-district-2'
SLUG_DISTRICT_SED = 'test-slug-district-SED'

TITLE_ENERGY_DISTRICT = 'Тестовый энергорайон'
TITLE_SECOND_ENERGY_DISTRICT = 'Тестовый энергорайон_2'

TITLE_DISTRICT = 'Тестовый район(источник)'
TITLE_DISTRICT_2 = 'Тестовый район(источник)-2'
TITLE_DISTRICT_SED = 'Тестовый район(источник) другого энергорайона!'

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


# <----- Запись в журнале обходов тепловых сетей ----->
POST_WLK_NUMBER = 1
POST_WLK_NUMBER_2 = 2
POST_WLK_NUMBER_SED = 1

TASK_WLK = 'Тестовое задание'
TASK_WLK_IN_EDIT_POST = 'Тестовое задание измененное'
TASK_WLK_SED = 'Тестовое задание другого энергорайона!'

TEXT_WLK = 'Тестовые замечания'
TEXT_WLK_2 = 'Тестовые замечания второй записи'
TEXT_WLK_SED = 'Тестовые замечания другого энергорайона!'

PLAN_WLK = 'Тестовые мероприятия'
PLAN_WLK_IN_EDIT_POST = 'Тестовые мероприятия измененные'
PLAN_WLK_SED = 'Тестовые мероприятия другого энергорайона!'

RESOLUTION_WALK = 'Тестовая резолюция'
RESOLUTION_WALK_2 = 'Тестовая резолюция 2'

RESOLUTION_ID = 1

TRANSFER_WLK = 'Тестовый перенос ремонта'
TRANSFER_WLK__IN_EDIT_POST = 'Тестовый перенос ремонта измененный'
TRANSFER_WLK_SED = 'Тестовый перенос ремонта другого энергорайона!'

WALK_DATE = datetime.date.today()
WALK_DATE_SED = datetime.date.today()
WALK_DATE_IN_EDIT_POST = datetime.date.today() - datetime.timedelta(days=1)
WALK_DATE_NOT_VALID = datetime.date.today() + datetime.timedelta(days=1)


# <----- Запись в журнале ремонтных работ ----->
POST_REPAIR_NUMBER = 1
POST_REPAIR_NUMBER_2 = 2
POST_REPAIR_NUMBER_SED = 3

ORDER_REPAIR = 'Наряд'
ORDER_REPAIR_2 = 'Распоряжение'
ORDER_REPAIR_SED = 'Наряд'

NUMBER_ORDER_REPAIR = 1
NUMBER_ORDER_REPAIR_2 = 2
NUMBER_ORDER_REPAIR_SED = 3

ADRESS_REPAIR = 'Ул. Тестовая 1'
ADRESS_REPAIR_2 = 'Ул. Тестовая 2'
ADRESS_REPAIR_SED = 'Ул. Тестовая 1 другого энергорайона!'

DESCRIPTION_REPAIR = 'Тестовые работы выполнены'
DESCRIPTION_REPAIR_2 = 'Тестовые работы выполнены 2'
DESCRIPTION_REPAIR_SED = 'Тестовые работы другого энергорайона!'

DATE_START_WORKING_REPAIR = datetime.date.today() - datetime.timedelta(days=1)
DATE_END_WORKING_REPAIR = datetime.date.today()

DATE_END_WORKING_REPAIR_NOT_VALID = DATE_START_WORKING_REPAIR - datetime.timedelta(days=1)

DATE_START_WORKING_REPAIR_2 = datetime.date.today() - datetime.timedelta(days=2)
DATE_END_WORKING_REPAIR_2 = DATE_START_WORKING_REPAIR_2 + datetime.timedelta(days=1)

DATE_START_WORKING_REPAIR_SED = datetime.date.today() - datetime.timedelta(days=1)
DATE_END_WORKING_REPAIR_SED = datetime.date.today()


# <----- Запись в журнале учета нарядов и распоряжений ----->
POST_ORDER_NUMBER = 1
POST_ORDER_NUMBER_2 = 2
POST_ORDER_NUMBER_SED = 3

ORDER_ORDER = 'Наряд'
ORDER_ORDER_2 = 'Распоряжение'
ORDER_ORDER_SED = 'Наряд'

NUMBER_ORDER_ORDER = 1
NUMBER_ORDER_ORDER_2 = 2
NUMBER_ORDER_ORDER_SED = 3

DESCRIPTION_ORDER = 'Тестовые наименования работ'
DESCRIPTION_ORDER_2 = 'Тестовые наименования работ 2'
DESCRIPTION_ORDER_SED = 'Тестовые наименования работ другого энергорайона!'

DATE_START_WORKING_ORDER = datetime.date.today() - datetime.timedelta(days=1)
DATE_END_WORKING_ORDER = datetime.date.today()

DATE_END_WORKING_ORDER_NOT_VALID = DATE_START_WORKING_ORDER - datetime.timedelta(days=1)

DATE_START_WORKING_ORDER_2 = datetime.date.today() - datetime.timedelta(days=2)
DATE_END_WORKING_ORDER_2 = DATE_START_WORKING_ORDER_2 + datetime.timedelta(days=1)

DATE_START_WORKING_ORDER_SED = datetime.date.today() - datetime.timedelta(days=1)
DATE_END_WORKING_ORDER_SED = datetime.date.today()


# <----- Реверсы  ----->
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
JRNL_REPAIR_WORK_REVERSE = 'office:journal_repair_work'
CREATE_POST_REPAIR_REVERSE = 'office:create_post_repair'
EDIT_POST_REPAIR_REVERSE = 'office:edit_post_repair'
JRNL_ORDER_REVERSE = 'office:journal_order'
CREATE_POST_ORDER_REVERSE = 'office:create_post_order'
EDIT_POST_ORDER_REVERSE = 'office:edit_post_order'


# <----- Урлы ----->
INDEX_URL = reverse(INDEX_REVERSE)
CABINET_URL = reverse(CABINET_REVERSE)
BRIGADES_URL = reverse(BRIGADES_REVERSE)
EMPLOYEES_URL = reverse(EMPLOYEES_REVERSE)
JOURNALS_URL = reverse(JOURNALS_REVERSE)
DISTRICTS_URL = reverse(DISTRICTS_REVERSE)
JRNL_REPAIR_WORK_URL = reverse(JRNL_REPAIR_WORK_REVERSE)
JRNL_ORDER_URL = reverse(JRNL_ORDER_REVERSE)
JRNL_WLK_URL = reverse(
    JRNL_WLK_REVERSE, kwargs={'slug_district': SLUG_DISTRICT}
)
CREATE_POST_WLK_URL = reverse(
    CREATE_POST_WLK_REVERSE,
    kwargs={
        'slug_district': SLUG_DISTRICT
    }
)
EDIT_POST_WLK_URL = reverse(
    EDIT_POST_WLK_REVERSE,
    kwargs={
        'slug_district': SLUG_DISTRICT,
        'post_id': POST_WLK_NUMBER
    }
)
ADD_RESOLUTION_URL = reverse(
    ADD_RESOLUTION_REVERSE,
    kwargs={
        'slug_district': SLUG_DISTRICT,
        'post_id': POST_WLK_NUMBER
    }
)
UPDATE_RESOLUTION_URL = reverse(
    UPDATE_RESOLUTION_REVERSE,
    kwargs={
        'slug_district': SLUG_DISTRICT,
        'post_id': POST_WLK_NUMBER,
        'resolution_id': RESOLUTION_ID
    }
)
CREATE_POST_REPAIR_URL = reverse(CREATE_POST_REPAIR_REVERSE)
EDIT_POST_REPAIR_URL = reverse(
    EDIT_POST_REPAIR_REVERSE,
    kwargs={
        'post_id': POST_REPAIR_NUMBER
    }
)
CREATE_POST_ORDER_URL = reverse(CREATE_POST_ORDER_REVERSE)
EDIT_POST_ORDER_URL = reverse(
    EDIT_POST_ORDER_REVERSE,
    kwargs={
        'post_id': POST_ORDER_NUMBER
    }
)


# <----- Адреса шаблонов ----->
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

JRNL_REPAIR_WORK_TMPL = 'office/journal_repair_work.html'
CREATE_POST_REPAIR_TMPLT = 'office/create_post_repair.html'
EDIT_POST_REPAIR_TMPLT = 'office/edit_post_repair.html'

JRNL_ORDER_TMPL = 'office/journal_order.html'
CREATE_POST_ORDER_TMPLT = 'office/create_post_order.html'
EDIT_POST_ORDER_TMPLT = 'office/edit_post_order.html'
