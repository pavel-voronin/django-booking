from django.shortcuts import get_object_or_404
from django.db.models import F, Q
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.db import transaction
from datetime import date
from django.db.models import Count

from .models import Hotel, Reservation, User, Room


def like_hotel_view_with_f(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    hotel.likes = F('likes') + 1
    hotel.save()
    return JsonResponse({'details': 'success'})


def dislike_hotel_view_with_f(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    hotel.dislikes = F('dislikes') + 1
    hotel.save()
    return JsonResponse({'details': 'success'})


def like_hotel_view_with_transaction(request, hotel_id):
    with transaction.atomic():
        hotel = Hotel.objects.select_for_update().get(id=hotel_id)
        hotel.likes += 1
        hotel.save()
    return JsonResponse({'details': 'success'})


def dislike_hotel_view_with_transaction(request, hotel_id):
    with transaction.atomic():
        hotel = Hotel.objects.select_for_update().get(id=hotel_id)
        hotel.dislikes += 1
        hotel.save()
    return JsonResponse({'details': 'success'})


def get_users_living_in_hotel_maryland(request):
    hotel = get_object_or_404(Hotel, title='Maryland')
    rooms = hotel.rooms.all()

    user_ids = Reservation.objects \
        .filter(room__in=rooms) \
        .values_list('user', flat=True)

    users = User.objects.filter(id__in=user_ids)
    result = [model_to_dict(user) for user in users]

    return JsonResponse({'details': 'success', 'users': result})


def get_rooms_list_with_sold_out_sign(request, move_in, move_out):
    # TODO check move_in and move_out dates

    rooms = Room.objects.all()

    rooms_list = []

    for room in rooms:
        sold_out = room.reservations \
            .filter(start__lte=move_out, end__gt=move_in) \
            .exists()

        room_serialized = model_to_dict(room, fields=['id', 'title'])
        room_serialized.update({"sold_out": sold_out})

        rooms_list.append(room_serialized)

    return JsonResponse({'details': 'success', 'rooms': rooms_list})


def get_hotels_with_one_free_room(request):
    today = date.today()
    hotels = Hotel.objects \
        .annotate(free_rooms=Count("rooms",
                                   filter=Q(rooms__reservations__start__gt=today) |
                                   Q(rooms__reservations__end__lte=today))) \
        .filter(
            free_rooms=1
        ).all()

    hotels_list = [model_to_dict(hotel) for hotel in hotels]

    return JsonResponse({'details': 'success', 'hotels': hotels_list})
