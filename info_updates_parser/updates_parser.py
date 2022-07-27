"""
Получает записи из БД с группами
и отправляет их на актуализацию
"""
import datetime
import os
import time

import django
from celery import shared_task

os.environ['DJANGO_SETTINGS_MODULE'] = 'vk_group_info.settings'
django.setup()
from django.conf import settings

from vk_groups.serializers import VkGroupSerializer
from vk_groups.models import VkGroupModel
from info_parser.vk_api_parser import get_group_info_from_api, parse_response
from vk_group_info.tasks import update_group


def get_groups() -> list:
    #  Минимальная время и дата обновления, чтобы записи,
    #  которые обновлены позднее этого времени не попадали в обработку.
    minimum_datetime = datetime.datetime.fromtimestamp(time.time() - settings.UPDATER_TIME_DELTA)
    groups = VkGroupModel.objects.filter(last_update_at__lte=minimum_datetime)
    groups = [VkGroupSerializer(group).data for group in groups]
    return groups


def start():
    while True:
        groups = get_groups()

        for group in groups:
            try:
                new_data = get_group_info_from_api(group["id"])
                new_data = parse_response(new_data)
                update_group.delay(group, new_data)
            except Exception as ex:
                print(ex)

        time.sleep(settings.SCHEDULER_REFRESH_TIME)


if __name__ == "__main__":
    start()
