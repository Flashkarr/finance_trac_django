INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.core',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'finance_db',
        'USER': 'postgres',
        'PASSWORD': '22882278002',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
    # 'default': {
    #         'ENGINE': 'django.db.backends.mysql',  # Використовуємо MySQL
    #         'NAME': 'finance_trac_db',  # Назва БД
    #         'USER': 'root',  # Ім'я користувача MySQL
    #         'PASSWORD': 'root',  # Пароль
    #         'HOST': 'localhost',  # Якщо БД локально
    #         'PORT': '3306',  # Стандартний порт MySQL
    #         'OPTIONS': {
    #             'charset': 'utf8mb4',  # Щоб працювали emoji та спецсимволи
    #         },
    #     },
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # },
}