# from django.contrib.staticfiles.storage import staticfiles_storage
from django.templatetags.static import static
from django.urls import reverse

from jinja2 import Environment


def environment(**options):
    env: Environment = Environment(**options)
    env.globals.update({
        'static': static,
        'url': reverse,
        'zip': zip,
    })
    return env

