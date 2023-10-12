from django.db import migrations


journals = [
    {
        'title': 'Журнал обходов тепловых сетей',
        'slug': 'zhurnal-obhodov-teplovyh-setej',
        'description': 'Журнал для регистрации обходов тепловых сетей'
    },
    {
        'title': 'Журнал ремонтных работ',
        'slug': 'zhurnal-remontnyh-rabot',
        'description': 'Журнал для записей выполненных ремонтных работ'
    },
    {
        'title': 'Журнал дефектов оборудования',
        'slug': 'zhurnal-defektov-oborudovaniya',
        'description': 'Журнал для учета дефектов и неполадок оборудования'
    },
]

def add_journal(apps, schema_editor):
    Journal = apps.get_model('office', 'Journal')
    journals_list = [
        Journal(title=journal['title'], slug=journal['slug'], description=journal['description']) for journal in journals
    ]
    Journal.objects.bulk_create(journals_list)


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0010_add_position'),
    ]

    operations = [
        migrations.RunPython(add_journal),
    ]
