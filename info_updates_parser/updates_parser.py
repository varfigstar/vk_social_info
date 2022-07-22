"""
Получает записи из БД с группами
и отправляет их на актуализацию
"""
import os
import time

import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'vk_group_info.settings'
django.setup()
from django.conf import settings

from vk_groups.serializers import VkGroupSerializer
from vk_groups.models import VkGroupModel
from info_parser.vk_api_parser import get_group_info_from_api, parse_response


def update_group_data(group_data):
    new_data = get_group_info_from_api(group_data["id"])
    new_data = parse_response(new_data)

    if new_data != group_data:
        group = VkGroupModel.objects.get(id=group_data["id"])
        group.title = new_data["title"]
        group.user_count = new_data["user_count"]
        group.save()


def get_groups() -> list:
    groups = VkGroupModel.objects.all()
    groups = [VkGroupSerializer(group).data for group in groups]
    return groups


def start():
    while True:
        groups = get_groups()

        for group in groups:
            try:
                update_group_data(group)
            except Exception as ex:
                print(ex)

        time.sleep(settings.SCHEDULER_REFRESH_TIME)


if __name__ == "__main__":
    start()
