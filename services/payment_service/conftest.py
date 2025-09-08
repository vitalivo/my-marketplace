import pytest
from django.core.management import call_command
from django.apps import apps

@pytest.fixture(scope='session')
def django_db_setup(django_db_blocker):
    """
    Гарантируем, что миграции применяются в тестовой БД.
    Фикстура запускается один раз за тестовую сессию.
    """
    with django_db_blocker.unblock():
        # Убедимся, что приложения Django инициализированы
        if not apps.ready:
            apps.populate(apps.get_app_configs())

        print("\nApplying migrations for test database...")
        # Применяем миграции без интерактивных вопросов
        call_command('migrate', verbosity=0, interactive=False)
        print("Migrations applied to test database.")