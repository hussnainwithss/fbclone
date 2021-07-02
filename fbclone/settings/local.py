from fbclone.settings.base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD', default=''),
        'HOST': env('DATABASE_HOST', default='localhost'),
        'PORT': env('DATABASE_PORT', default='5432'),
    }
}

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST= 'smtp.google.com'
# EMAIL_PORT: 587
# EMAIL_HOST_USER=env('EMAIL_USERNAME')
# EMAIL_HOST_PASSWORD=env('EMAIL_PASSWORD')
# EMAIL_USE_TLS = True

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# change this to a proper location
EMAIL_FILE_PATH = BASE_DIR / 'tmp/app-messages'
