from django.db import models


class Account(models.Model):
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=256)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
