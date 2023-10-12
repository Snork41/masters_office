from django.db import migrations


districts = [
    {
        'title': 'Котельная № 1 "Ленина"',
        'slug': 'kotelnaya-1-lenina',
        'master': 'Testuser'
    },
    {
        'title': 'Котельная № 2 "Снежная"',
        'slug': 'kotelnaya-2-snezhnaya',
        'master': 'Testuser'
    },
    {
        'title': 'ЦТП № 67 "8 километр"',
        'slug': 'ctp-67-8-kilometr',
        'master': 'Testuser'
    },
]

def add_district(apps, schema_editior):
    User = apps.get_model('users', 'CustomUser')
    District = apps.get_model('office', 'District')
    districts_list = []
    for district in districts:
        districts_list.append(
            District(
                title=district['title'],
                slug=district['slug'],
                master=User.objects.get(username=district['master'])
            )
        )
    District.objects.bulk_create(districts_list)


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0012_add_personal'),
        ('users', '0002_add_test_user'),
    ]

    operations = [
        migrations.RunPython(add_district)
    ]
