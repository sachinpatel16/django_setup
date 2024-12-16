import re
from rest_framework import serializers
from django.db.models import Q


class UniqueNameMixin:
    """
        Mixin for validating unique name or type at add and update time.
    """

    def validate_name(self, value):
        return self.validate_unique_field('name', value)

    def validate_type(self, value):
        return self.validate_unique_field('type', value)

    def validate_department_name(self, value):
        return self.validate_unique_field('department_name', value)

    def validate_area_name(self, value):
        return self.validate_unique_field('area_name', value)

    def validate_serving_info(self, value):
        return self.validate_unique_field('serving_info', value)

    def validate_unique_field(self, field_name, value):
        """
            Validate that the field (`name` or `type`) is unique for the given model.
        """
        method = self.context['request'].method
        model = self.Meta.model
        url_path =self.context['request'].path
        pattern = r'/([^/]+)/$'
        match = re.search(pattern, url_path)
        if match and match.group(1) == 'patch_data':
            exclude_filter = {
                f'{field_name}__iexact': getattr(self.instance, field_name, None)} if self.instance else {}
            if model.objects.exclude(**exclude_filter).filter(**{f'{field_name}__iexact': value}).exists():
                verbose_name = model._meta.verbose_name
                raise serializers.ValidationError(f"{verbose_name} with that {field_name} already exists.")

        elif method == "POST" and model.objects.filter(**{f'{field_name}__iexact': value}).exists():
            verbose_name = model._meta.verbose_name
            raise serializers.ValidationError(f"{verbose_name} with that {field_name} already exists.")

        return value

    def update(self, instance, validated_data):
        """
            Ensure the updated name or type is unique.
        """
        # if 'name' in validated_data and validated_data['name'].lower() != instance.name.lower():
        #     self.check_unique_field(instance, validated_data, 'name')
        #
        # elif 'type' in validated_data and validated_data['type'].lower() != instance.type.lower():
        #     self.check_unique_field(instance, validated_data, 'type')
        #
        # elif 'department_name' in validated_data and validated_data['department_name'].lower() != instance.department_name.lower():
        #     self.check_unique_field(instance, validated_data, 'department_name')
        #
        # elif 'area_name' in validated_data and validated_data['area_name'].lower() != instance.area_name.lower():
        #     self.check_unique_field(instance, validated_data, 'area_name')
        #
        # elif 'serving_info' in validated_data and validated_data['serving_info'].lower() != instance.serving_info.lower():
        #     self.check_unique_field(instance, validated_data, 'serving_info')

        for field_name in ['name', 'type', 'department_name', 'area_name', 'serving_info']:
            if field_name in validated_data:
                field_value = validated_data[field_name]
                if getattr(instance, field_name).lower() != field_value.lower():
                    self.check_unique_field(instance, validated_data, field_name)

        return super().update(instance, validated_data)

    def check_unique_field(self, instance, validated_data, field_name):
        """
            Check if the field (`name` or `type`) is unique for the given instance and validated data.
        """
        model = self.Meta.model
        if model.objects.filter(~Q(pk=instance.pk), **{f'{field_name}__iexact': validated_data[field_name]}).exists():
            verbose_name = model._meta.verbose_name
            raise serializers.ValidationError(f"A {verbose_name} with that {field_name} already exists.")
