from django.http import JsonResponse
from functools import wraps
from main.models import Room
import json

def check_permission(func):
    @wraps(func)
    def wrapper_decorator(request, *args, **kwargs):
        user = request.user
        try:
            if kwargs:
                room_name = kwargs['room_name']
                room = Room.objects.get(room=room_name)  
            else:
                json_str = request.body.decode(encoding='UTF-8')
                data_json = json.loads(json_str)
                room = Room.objects.get(room=data_json['room_name'])


            user_admin = room.user_admin
            if user != user_admin:
                reponse = {
                    "status": False,
                    "message": "Access denied"
                }
                return JsonResponse(reponse)
        except Exception as e:
            response = {"status": False}
            response['message'] = f'{e.__class__.__name__}'
            return JsonResponse(response)
        return func(request, *args, **kwargs)
    return wrapper_decorator