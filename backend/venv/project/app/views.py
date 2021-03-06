from django.shortcuts import render

from django.http import JsonResponse, HttpResponse

from .models import *
from .serializers import *

import json

# Create your views here.
def index_view(req):
    req.session['current_room'] = 1
    return render(req, 'index.html')

def current_room(req):
    current_room = req.session.get('current_room')
    return HttpResponse(current_room if current_room else '')
def get_initial_room_data(req):
    current_room = req.session.get('current_room')

    room_object_list = Room.objects.filter(pk=current_room)
    if room_object_list:
        room_object = room_object_list[0]

        room_users = UserInRoom.objects.filter(room=room_object)
        user_positions = list(map(
            lambda room_user: room_user.user_position,
            room_users
        ))

        # Create initial data dictionary
        initial_data = []
        for room_user in room_users:
            def user_matches_position(user_position):
                user_in_room = user_position.userinroom_set.all()[0]
                user_instance = room_user.user

                return user_in_room.user == user_instance
            user_position = list(filter(
                lambda room_user: user_matches_position(room_user),
                user_positions
            ))[0]
            user_id = room_user.user.id

            user_position_serializer = UserPositionSerializer(user_position)
            user_position_dict = user_position_serializer.data

            user_data = {
                'position': user_position_dict,
                'user_id': user_id
            }
            initial_data.append(user_data)
    else:
        initial_data = []

    return JsonResponse({'data': initial_data})
def get_user(req, id):
    if User.objects.filter(pk=id):
        # Get user details
        user = User.objects.get(pk=id)

        serializer = UserSerializer(user)
        user_dict = serializer.data

        # Get user profile details
        user_profile = user.userprofile_set.all()[0]
        user_profile_dict = UserProfileSerializer(user_profile).data

        user_data = {
            'user': user_dict,
            'user_profile': user_profile_dict
        }
    else:
        user_data = ''

    return JsonResponse(user_data)
