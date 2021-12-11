from django.contrib.auth.models import AbstractUser
from django.db import models
from config.settings import MEDIA_URL, STATIC_URL

IMAGEN_VACIA = 'img/empty.png'


class User(AbstractUser):
    image = models.ImageField(upload_to='users/', null=True, blank=True)

    def get_image(self):
        if self.image:
            return f'{MEDIA_URL}{self.image}'
        return f'{STATIC_URL}{IMAGEN_VACIA}'



