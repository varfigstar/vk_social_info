from django.test import TestCase

from .updates_parser import get_groups
from vk_groups.models import VkGroupModel
from vk_group_info.tasks import update_group


class UpdatesParserTestCase(TestCase):
    def setUp(self) -> None:
        VkGroupModel.objects.create(id="it_joke_test", user_count=100, title="IT Юмор")

    def test_get_groups(self):
        groups = get_groups()

        keys = []

        for group in groups:
            keys.append(group["id"])

        assert "it_joke_test" in keys

    def test_update_group_data(self):
        test_data = dict(id="it_joke", user_count=100, title="IT Юмор")
        VkGroupModel.objects.create(**test_data)
        update_group.run(test_data)
        group = VkGroupModel.objects.get(id=test_data["id"])
        assert group.user_count > test_data["user_count"]

