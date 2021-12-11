from django.db import models
from django.conf import settings


class BaseModel(models.Model):
    # Campos de auditoría
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='%(app_label)s_%(class)s_creation',
                                      null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                     related_name='%(app_label)s_%(class)s_updated',
                                     null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True
