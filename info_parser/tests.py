import asyncio
import json

from django.test import TestCase

from .vk_api_parser import get_group_info_from_api, GroupNotFoundException, Parser
from vk_groups.models import VkGroupModel


class TestParser(TestCase):

    def setUp(self) -> None:
        VkGroupModel.objects.create(id="it_joke", user_count=100, title="IT mems")
        self.parser = Parser()
        self.parser.ex_time = 1

    def test_get_group_info(self):
        group_id = "it_joke"
        data = get_group_info_from_api(group_id)
        assert isinstance(data, dict)

    def test_get_group_info_with_error(self):
        group_id = "it_joke11"
        data = None
        try:
            data = get_group_info_from_api(group_id)
        except GroupNotFoundException:
            assert data is None

    def test_get_data_from_redis(self):
        test_data = {
                "id": "it_joke111",
                "user_count": 100,
                "title": "test title"
            }
        asyncio.run(self.parser.create_new_group(
            test_data["id"],
            test_data
        ))
        self.parser.redis_cli.set(test_data["id"], json.dumps(test_data), ex=self.parser.ex_time)

        result = self.parser._get_data_from_redis(group_id=test_data["id"])

        assert result == test_data

    def test_get_info_from_db(self):
        test_data = {
            "id": "db_test",
            "user_count": 110,
            "title": "test title db"
        }
        
        asyncio.run(
            self.parser.create_new_group(
                test_data["id"],
                test_data
            )
        )
        
        result = asyncio.run(self.parser._get_data_from_db(test_data["id"]))

        assert result == test_data
