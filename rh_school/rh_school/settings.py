from pathlib import Path

# Chemin de base du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# Clé secrète pour Django (à garder confidentielle en production)
SECRET_KEY = 'django-insecure-(rw)u0vup73rj2d5^y7rf339g*a=#5qkif$6+-uax_k#=p_#cr'

# Mode DEBUG actif pour le développement
DEBUG = True

# Hôtes autorisés
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Applications installées
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gestion_rh',  # Ton application
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuration des URLs principales
ROOT_URLCONF = 'rh_school.urls'

# Configuration des templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'gestion_rh' / 'templates'  # ✅ Où se trouvent les dossiers 'gestion_rh', 'employe', 'rh', etc.
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = 'rh_school.wsgi.application'

# Base de données PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gestion_rh',
        'USER': 'eva',
        'PASSWORD': 'isep',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Validation des mots de passe
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Langue et fuseau horaire
LANGUAGE_CODE = 'fr-FR'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Fichiers statiques (CSS, JS, etc.)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'gestion_rh' / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Pour production avec collectstatic

# Authentification
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

# Modèle ID auto par défaut
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
