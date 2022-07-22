from django.contrib import admin

from .models import VkGroupModel


@admin.register(VkGroupModel)
class VkGroupAdmin(admin.ModelAdmin):
    ...

