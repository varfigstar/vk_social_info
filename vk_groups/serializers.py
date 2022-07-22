from rest_framework.serializers import ModelSerializer

from .models import VkGroupModel


class VkGroupSerializer(ModelSerializer):
    class Meta:
        model = VkGroupModel
        fields = ["id", "title", "user_count"]
