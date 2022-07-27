from django.db import models


class VkGroupModel(models.Model):
    id = models.CharField(max_length=355, primary_key=True)
    title = models.CharField(max_length=355)
    user_count = models.IntegerField()
    last_update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} | {self.title}'

    class Meta:
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["last_update_at"]),
        ]
