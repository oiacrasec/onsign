from django.db import models

from base.models import BaseModel


class Tracker(BaseModel):
    location = models.CharField(verbose_name='Location', max_length=40)
    ip_address = models.GenericIPAddressField(verbose_name='IP Address', editable=False)
    consulted = models.BooleanField(verbose_name='Consulted', default=True, editable=False)

    def __str__(self):
        return '{ip}: {created_at}'.format(
            ip=self.ip_address, created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        )

    class Meta:
        db_table = 'onsign_tracker'
