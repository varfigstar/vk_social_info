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


@shared_task
def update_group(group_data, new_data):
    group = VkGroupModel.objects.get(id=group_data["id"])

    if new_data != group_data:
        group.title = new_data["title"]
        group.user_count = new_data["user_count"]
        group.save()
    else:
        group.save()
