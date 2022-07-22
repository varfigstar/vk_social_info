from django.conf import settings

import requests


API_VERSION = "5.131"


def create_url(access_token: str, method: str):
    return "https://api.vk.com/method/{}?PARAMS&access_token={}&v={}".format(
        method, access_token, API_VERSION
    )


def get_group_info_from_api(group_id: str):
    """
    Получает информацию сообщества от API
    """
    url = create_url(settings.VK_API_ACCESS_TOKEN, "groups.getById")
    resp = requests.get(url, params={"group_id": group_id})
    return resp.json()["response"][0]


