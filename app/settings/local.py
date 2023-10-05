from .base import *  # noqa:F403

DEBUG = True
ENVIRONMENT = "local"

DEVELOPMENT_APPS = ["django_extensions"]
INSTALLED_APPS += DEVELOPMENT_APPS  # noqa:F405
