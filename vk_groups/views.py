from django.http import JsonResponse

from info_parser.vk_api_parser import Parser


parser = Parser()


async def get_group_info(request, id: str):
    try:
        parser.start_task()
        data = await parser.get_group_info(group_id=id)
    except Exception as ex:
        return JsonResponse({"error": str(ex)})
    finally:
        parser.ack_task()

    return JsonResponse(data)


async def get_tasks_counter(requst):
    return JsonResponse(
        {"tasks_counter": parser.get_tasks_counter()}
    )
