"""
Celery таски для взаимодействия с БД
"""

from celery import shared_task

from vk_groups.models import VkGroupModel


@shared_task
def create_new_group(data: dict):
    VkGroupModel.objects.create(**data)
