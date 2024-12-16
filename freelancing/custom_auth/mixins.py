from django.db import models

from freelancing.utils.utils import get_user_photo_random_filename


class UserPhotoMixin(models.Model):
    photo = models.ImageField(
        upload_to=get_user_photo_random_filename,
        height_field="height_photo",
        width_field="width_photo",
        null=True,
        blank=True,
    )

    width_photo = models.PositiveSmallIntegerField(blank=True, null=True)
    height_photo = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        abstract = True
