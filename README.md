# Кабинет мастера (Masters Office)

### Технологии:
Python 3.10
Django 4.2.6

### Описание:

Кабинет мастера позволяет вести инженерно-техническим работникам теплоснабжающих организаций рабочую документацию в электронном виде.

<hr>

### Планирумый функционал приложения:

 - [ ] Раздел для ведения электроных журналов таких как: 
    - [x] журнал обхода и осмотра тепловых сетей;
    - [ ] журнал ремонтных работ;
    - [ ] журнал дефектов оборудования;
    - [ ] журнал проработки директивных материалов;
    - [ ] журнал регистрации инструктажей;
    - [ ] журнал противоаварийных и противопожарных тренировок;
    - [ ] журнал учета проверки знаний норм и правил;
    - [ ] журнал проверки средств пожаротушения;

            
- [ ] Ведение паспортов тепловых сетей и ЦТП

- [x] Раздел с отображением существующих бригад
    
- [ ] Ведение учета выдачи спецодежды и средств индивидуальной защиты (СиЗ) персоналу

- [x] Раздел с таблицей всех сотрудников района (с фильтрацией и сортировкой)

- [ ] Хранение справочной информации


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
        - состояние удаления записи (помечена ли на удаление)
    - **резолюции**:
        - Для какой записи резолюция
        - Автор
        - Резолюция начальника энергорайона (поле для текста)

2. В самом **приложении** доступны:
    - регистрация пользователя;
    - восстановление пароля (через email).  
    При _DEBUG = True_ письма приходят в masters_office/sent_emails. При _DEBUG = False_ письмо придёт непосредственно на почту;
    - авторизация по имени и паролю;
    - журнал обходов тепловых сетей, в котором можно:
        - создать запись;
        - отредактировать её;
        - начальник района (юзер с необходимыми правами) может оставлять свои резолюции к этим записям;
        - запись можно оттмечать как "удаленную";
    - в журнале обходов реализована пагинация.

3. При выполнении миграций в базу данных будет загруженны _демонстрационные_ записи следующих моделей:
    - Энергорайонов (первый энергорайон, второй энергорайон...)
    - Должностей (начальник, сесарь и т.д.)
    - Журналов
    - Персонала (несколько сотрудников)
    - Источников тепла (котельные, цтп)
    - Один тестовый пользователь (в должности мастера)
    Для авторизации под этим пользователем используйте:
    ```
    Имя: Testuser 
    Пароль: testuser12345
    ```

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
    ```
- В директории с файлом **manage.py** создайте .env файл и сохраните в нем свой SECRET_KEY (например, сгенерируйте его на https://djecrety.ir/):
    ```
    touch .env
    ```
    _Пример оформления файла .env можно посмотреть в .env_example_

- В директории с файлом **manage.py** выполните миграции:
    ```
    python manage.py migrate
    ```
- Создайте суперюзера:
    ```
    python manage.py createsuperuser
    ```
- Запустите проект:
    ```
    python manage.py runserver
    ```

---
#### Автор:
__[Максим Давлеев](https://github.com/Snork41)__
