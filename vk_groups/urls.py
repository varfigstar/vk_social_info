from django.urls import path

from . import views

urlpatterns = [
    path('group/<str:id>/', views.get_group_info),
]
