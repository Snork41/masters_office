# Generated by Django 4.1.7 on 2023-03-16 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Источник тепла')),
                ('slug', models.SlugField(default='DEFAULT VALUE', unique=True)),
            ],
            options={
                'verbose_name': 'Источник тепла',
                'verbose_name_plural': 'Источники тепла',
            },
        ),
        migrations.CreateModel(
            name='EnergyDistrict',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='Энергорайон')),
            ],
            options={
                'verbose_name': '"Энергорайон"',
                'verbose_name_plural': 'Энергорайоны',
            },
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Журнал',
                'verbose_name_plural': 'Журналы',
            },
        ),
        migrations.CreateModel(
            name='Personal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('middle_name', models.CharField(max_length=50, verbose_name='Отчество')),
                ('rank', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)], null=True, verbose_name='Разряд')),
                ('tab_number', models.SmallIntegerField(blank=True, null=True, unique=True, verbose_name='Табельный номер')),
            ],
            options={
                'verbose_name': 'Работник',
                'verbose_name_plural': 'Работники',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_position', models.CharField(max_length=30, verbose_name='Должность')),
            ],
            options={
                'verbose_name': 'Должность',
                'verbose_name_plural': 'Должности',
            },
        ),
        migrations.CreateModel(
            name='PostWalking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_post', models.PositiveIntegerField(default=1, verbose_name='Номер записи')),
                ('pub_date', models.DateTimeField(verbose_name='Дата обхода')),
                ('task', models.TextField(default='Обход тепловой сети', max_length=250, verbose_name='Участок теплотрассы, задание мастера')),
                ('text', models.TextField(help_text='Введите текст записи', verbose_name='Замечания, выявленные при обходе')),
                ('plan', models.TextField(blank=True, default='---', verbose_name='Организационные мероприятия по устранению')),
                ('resolution', models.TextField(blank=True, default='---', verbose_name='Резолюция начальника энергорайона')),
                ('fix_date', models.DateField(blank=True, null=True, verbose_name='Дата устранения замечания')),
                ('transfer', models.CharField(blank=True, default='---', max_length=150, verbose_name='Перенос на ремонт в план на следующий месяц или на межотопительный период')),
            ],
            options={
                'verbose_name': 'Запись',
                'verbose_name_plural': 'Записи',
            },
        ),
    ]
