from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SQLITE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'dbsweb.sqlite3',
    }
}

POSTGRESQL = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('POSTGRE_NAME'),
        'USER': config('POSTGRE_USER'),
        'PASSWORD': config('POSTGRE_PSWD'),
        'HOST': config('POSTGRE_HOST'),
        'PORT': config('POSTGRE_PORT')
    }
}
