from django.urls import path, register_converter
from datetime import datetime, date

from . import views


class DateConverter:
    regex = '[0-9]{4}-[0-9]{2}-[0-9]{2}'

    def to_python(self, value: str):
        return datetime.strptime(value, '%Y-%m-%d').date()

    def to_url(self, value: date):
        return value.strftime('%Y-%m-%d')


register_converter(DateConverter, 'date')

app_name = 'booking'
urlpatterns = [
    # 1. Get the list of users are living in hotel Maryland

    path('maryland', views.get_users_living_in_hotel_maryland, name='maryland'),

    # 2. fixed and improved like_hotel and dislike_hotel views (in terms of concurrency)

    # 2.1 Using F()

    path('like_f/<int:hotel_id>', views.like_hotel_view_with_f, name="like_hotel_f"),
    path('dislike_f/<int:hotel_id>',
         views.dislike_hotel_view_with_f, name="dislike_hotel_f"),

    # 2.2 Using transactions

    path('like_t/<int:hotel_id>', views.like_hotel_view_with_transaction,
         name="like_hotel_transaction"),
    path('dislike_t/<int:hotel_id>',
         views.dislike_hotel_view_with_transaction, name="dislike_hotel_transaction"),

    # 3. Get list of all rooms with sold_out(True|False) sign (attribute of
    # room object). Sold_out sign should be calculated for user’s move in
    # and move out dates.

    path('sold_out_rooms/<date:move_in>/<date:move_out>', views.get_rooms_list_with_sold_out_sign,
         name='sold_out_rooms'),

    # 4. Get list of hotels with only one free room (for today)

    path('hot_deals', views.get_hotels_with_one_free_room, name='hot_deals'),
]
