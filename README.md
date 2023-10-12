# Кабинет мастера (Masters Office)

### Технологии:
Python 3.10
Django 4.1.7

### Описание:

Кабинет мастера позволяет вести инженерно-техническим работникам теплоснабжающих организаций рабочую документацию в электронном виде.

<hr>

#### Планирумый функционал приложения:

1. Ведение электроных журналов таких как: 
    - журнал обхода и осмотра тепловых сетей;
    - журнал ремонтных работ;
    - журнал дефектов оборудования;
    - журнал проработки директивных материалов;
    - журнал регистрации инструктажей;
    - журнал противоаварийных и противопожарных тренировок;
    - журнал учета проверки знаний норм и правил;
    - журнал проверки средств пожаротушения;
    - и прочие

2. Ведение паспортов тепловых сетей и ЦТП
3. Формирование бригад
4. Ведение учета выдачи спецодежды и средств индивидуальной защиты (СиЗ) персоналу
5. Хранение справочной информации

#### На данный момент реализовано:
1. Через **панель адиминистратора** можно создавать, удалять, редактировать:
    - **пользователей** (сотрудников руководящих должностей, непосредственно юзеров) с присвоением должности;
    - **должности** (мастер, начальник и т.д.) с возможностью выбора участия в обходах тепловых сетей или нет;
    - **энергорайоны** (например 1 энергорайон, 5 энергорайон, Сетевой район и т.д.);
    - **источники тепла** (котельная № N, ЦТП № N) с присвоением ответственного лица. Slug заполняется автоматически;
    - **работников** (рабочие должности) с полями:
        - имя
        - фамилия
        - отчество
        - энергорайон
        - должность
        - разряд (1-7)
        - табельный номер (уникальный)
    - **бригады**:
        - номер
        - мастер бригады
        - бригадир
        - члены бригады
    - **журналы** (slug заполняется автоматически):
        - название (журнал обходов тепловых сетей, журнал ремонтных работ и т.д.)
        - описание
    - **записи в журнале обхода**:
        - порядковый номер записи (создается автоматически)
        - журнал, в котором будет запись
        - автор записи
        - источник тепла
        - дата создания записи (заполняется автоматически)
        - дата редактирования записи(заполняется автоматически)
        - чекбоксы "Плановый" и "Внеплановый" (обход тепловых сетей)
        - дата и время обхода
        - члены бригады
        - участок теплотрассы, задание мастера
        - замечания, выявленные при обходе
        - организационные мероприятия по устранению
        - дата устранения замечания
        - перенос на ремонт в план на следующий месяц или на межотопительный период
        - резолюция начальника энергорайона
    - **резолюции**:
        - Для какой записи резолюция
        - Автор
        - Резолюция начальника энергорайона (поле для текста)

2. В самом **приложении** доступны:
    - регистрация пользователя;
    - восстановление пароля (эмуляция работы почтового сервиса);
    - авторизация по имени и паролю;
    - журнал обходов тепловых сетей, в котором можно создать запись или отредактировать её. Начальник района (пользователь с правами) может оставлять свои резолюции к этим записям.

### Запуск приложения в режиме разработки:
- Клонируйте репозиторий:
    ```
    SSH: git clone git@github.com:Snork41/masters_office.git
    HTTPS: https://github.com/Snork41/masters_office.git
    ```
- Создайте и активируйте виртуальное окружение (версия Python должна быть не меньше 3.10):
    ```
    python -m venv venv
    source venv/Scripts/activate
    ```
- Установите зависимости из файла __requirements.txt__:
    ```
    pip install -r requirements.txt
    ````
- Создайте .env файл и сохраните в нем свой SECRET_KEY:
    ```
    touch .env
    ````
- В директории с файлом **manage.py** выполните миграции:
    ```
    python manage.py migrate
    ````
- Создайте суперюзера:
    ```
    python manage.py createsuperuser
    ````
- Запустите проект:
    ```
    python manage.py runserver
    ```

---
#### Автор:
__[Максим Давлеев](https://github.com/Snork41)__
