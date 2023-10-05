from importlib import import_module

from django.conf import settings


def autodiscover():
    """
    Perform an autodiscover of an viewsets.py file in the installed apps to
    generate the routes of the registered viewsets.
    """
    for app in settings.LOCAL_APPS:
        try:
            import_module(".".join((app, "viewsets")))
        except ImportError:
            pass
