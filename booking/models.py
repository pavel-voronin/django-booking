from django.db import models


class User(models.Model):
    pass


class Hotel(models.Model):
    title = models.CharField(max_length=128)
    likes = models.PositiveIntegerField()
    dislikes = models.PositiveIntegerField()


class Room(models.Model):
    title = models.CharField(max_length=128)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE,
                              related_name='rooms')


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE,
                             related_name='reservations')
    start = models.DateField()
    end = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='reservations')
