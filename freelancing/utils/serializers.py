from copy import copy
from decimal import Decimal
from typing import Any, Type
from django.utils.translation import gettext_lazy as _

from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError



def add_serializer_mixin(
    original: Type[serializers.Serializer], mixin: Any
) -> Type[serializers.Serializer]:
    if not hasattr(original, "Meta"):
        return original

    meta = type("NewMeta", (original.Meta,), {})

    for key, value in mixin.Meta.__dict__.items():
        if key.startswith("__"):
            continue

        if key == "fields":
            meta.fields = meta.fields + value
        elif key == "read_only_fields":
            if value == serializers.ALL_FIELDS:
                meta.read_only_fields = copy(meta.fields)
            else:
                meta.read_only_fields = meta.read_only_fields + value
        else:
            raise NotImplementedError(
                "Please specify desired behavior for {}".format(key)
            )

    extra_kwargs = {
        key: value
        for key, value in mixin.__dict__.items()
        if not key.startswith("__") and key != "Meta"
    }
    extra_kwargs["Meta"] = meta

    return type(
        "{}With{}".format(original.__name__, mixin.__name__), (original,), extra_kwargs
    )
