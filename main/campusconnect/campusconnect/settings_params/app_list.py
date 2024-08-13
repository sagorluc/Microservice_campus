# INSTALLED APPS
################

PREREQ_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "crispy_forms",
    "django.contrib.postgres",
    "django_elasticsearch_dsl",
    "django_elasticsearch_dsl_drf",
    # 'django_redis',
    # "storages",
    # "debug_toolbar", 
    # "corsheaders", 
 

]

CUSTOM_APPS = [
   
    "mmhauth",
    "guestactions",
    "mydocumentations",
    "superadmin",
    "viewtracker",
    "inventory",
    "general",
    'mymailroom',
    'systemops',
    'productops',
    
]




INSTALLED_APPS = PREREQ_APPS + CUSTOM_APPS

