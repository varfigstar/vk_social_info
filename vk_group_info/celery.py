import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vk_group_info.settings")
app = Celery("vk_group_info")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
