from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(verbose_name='Updated at', auto_now=True, editable=False)

    @classmethod
    def meta(cls):
        return cls._meta

    class Meta:
        abstract = True
