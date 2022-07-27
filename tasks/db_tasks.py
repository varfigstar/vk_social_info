"""
Celery таски для взаимодействия с БД
"""

import os

import django
from celery import shared_task

os.environ['DJANGO_SETTINGS_MODULE'] = 'vk_group_info.settings'
django.setup()

from vk_groups.models import VkGroupModel


@shared_task
def create_new_group(data: dict):
    VkGroupModel.objects.create(**data)
