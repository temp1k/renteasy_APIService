import dj_database_url
from decouple import config

from api.settings import *

SECRET_KEY = config('SECRET_KEY')

DATABASES['default'] = dj_database_url.parse(config('DATABASE_URL'))

ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(' ')
