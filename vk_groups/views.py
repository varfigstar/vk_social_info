from django.http import JsonResponse

from info_parser.vk_api_parser import Parser


parser = Parser()


async def get_group_info(request, id: str):
    try:
        data = await parser.get_group_info(group_id=id)
    except Exception as ex:
        raise ex

    return JsonResponse(data)

