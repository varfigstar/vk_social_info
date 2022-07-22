from django.test import TestCase

from .vk_api_parser import get_group_info_from_api


class TestParser(TestCase):
    def test_get_group_info(self):
        group_id = "it_joke"
        data = get_group_info_from_api(group_id)
        print(data)
        assert isinstance(data, dict)

