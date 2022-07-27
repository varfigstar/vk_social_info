import json

import requests
from redis import Redis
from django.conf import settings
from asgiref.sync import sync_to_async

from vk_groups.models import VkGroupModel
from vk_groups.serializers import VkGroupSerializer
from tasks.db_tasks import create_new_group


API_VERSION = "5.131"


class GroupNotFoundException(Exception):
    ...


def create_url(access_token: str, method: str):
    return "https://api.vk.com/method/{}?PARAMS&access_token={}&v={}".format(
        method, access_token, API_VERSION
    )


def get_group_info_from_api(group_id: str) -> dict:
    """
    Получает информацию сообщества от API
    """
    url = create_url(settings.VK_API_ACCESS_TOKEN, "groups.getById")
    resp = requests.get(url, params={"group_id": group_id, "fields": "members_count"}).json()
    resp_data = resp.get("response")
    if not resp_data:
        error = resp.get("error").get("error_msg")
        raise GroupNotFoundException(error)

    return resp_data[0]


def parse_response(response_data: dict):
    group_data = dict()
    group_data["id"] = response_data["screen_name"]
    group_data["title"] = response_data["name"]
    group_data["user_count"] = response_data["members_count"]
    return group_data


class Parser:
    def __init__(self):
        self.redis_cli = Redis.from_url(settings.REDIS_URL)
        self.ex_time = settings.REDIS_EX_TIME
        tasks_counter = self.redis_cli.get("TASKS_COUNTER")
        if not tasks_counter:
            self.redis_cli.set("TASKS_COUNTER", 0)

    def start_task(self):
        counter = int((self.redis_cli.get("TASKS_COUNTER")))
        self.redis_cli.set("TASKS_COUNTER", counter+1)

    def ack_task(self):
        counter = int(self.redis_cli.get("TASKS_COUNTER"))
        self.redis_cli.set("TASKS_COUNTER", counter-1)

    def get_tasks_counter(self) -> int:
        return int((self.redis_cli.get("TASKS_COUNTER")))

    def _get_data_from_redis(self, group_id: str) -> dict:
        data = self.redis_cli.get(group_id)

        if data:
            return json.loads(data)

    async def _get_data_from_db(self, group_id: str) -> dict:
        try:
            data = await sync_to_async(VkGroupModel.objects.get, thread_sensitive=True)(id=group_id)
        except Exception as ex:
            return
        if data:
            data = VkGroupSerializer(data, many=False).data
            return data

    def create_new_group(self, data: dict):
        task = create_new_group.delay(data)
        return task

    async def get_group_info(self, group_id: str) -> dict:
        data = self._get_data_from_redis(group_id)
        cached = bool(data)
        if not data:
            data = await self._get_data_from_db(group_id)
        if not data:
            data = get_group_info_from_api(group_id)
            data = parse_response(data)
            self.create_new_group(data)

        if not cached:
            self.redis_cli.set(group_id, json.dumps(data), ex=self.ex_time)

        return data
