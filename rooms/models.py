from django.db import models
from django.contrib.auth.hashers import make_password
from core.models import User
import uuid


class Room(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(
        max_length=200, null=True, blank=True, default='')
    admin = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='rooms_created')
    members = models.ManyToManyField(
        User, blank=True, related_name="rooms_joined")
    image = models.ImageField(
        null=True, blank=True, default='default.png')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)
        super(Room, self).save(*args, **kwargs)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "members": [user.serialize() for user in self.members.all()],
            "admin": self.admin.name,
            "image": self.image.url,
            "created": self.created.strftime("%b %d %Y, %I:%M %p"),
        }

    def __str__(self) -> str:
        return self.name


class RoomMessage(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_messages')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_messages')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]


    def serialize(self):
        return {
            "content": self.content,
            "user": self.user,
            "room": self.room,
            "created": self.created.strftime("%b %d %Y, %I:%M %p"),
        }

    def __str__(self) -> str:
        return f"{self.user} - {self.room} - {self.created}"
