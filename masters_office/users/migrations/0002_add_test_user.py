from django.db import migrations


def add_test_user(apps, schema_editor):
    Position = apps.get_model('office', 'Position')
    User = apps.get_model('users', 'CustomUser')
    User.objects.create_user(
        username='Testuser',
        password='testuser12345123',
        first_name='Тестовый',
        last_name='Пользователь',
        email='testuser@testuser.testuser',
        position=Position.objects.get(name_position='Мастер')
    )


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('office', '0012_add_personal'),
    ]

    operations = [
        migrations.RunPython(add_test_user)
    ]
