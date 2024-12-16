from drf_yasg.inspectors import SerializerInspector


class CustomSerializerInspector(SerializerInspector):
    def get_schema(self, serializer):
        schema = super().get_schema(serializer)
        if not getattr(schema, 'ref_name', None):
            schema.ref_name = serializer.__name__
        return schema
