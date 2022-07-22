from django.db import models


class VkGroupModel(models.Model):
    id = models.CharField(max_length=355, primary_key=True)
    title = models.CharField(max_length=355)
    user_count = models.IntegerField()

    def __str__(self):
        return f'{self.id} | {self.title}'


