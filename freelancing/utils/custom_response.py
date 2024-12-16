from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

from rest_framework import permissions
from .permissions import IsAPIKEYAuthenticated

class CustomMessageResponseMixin:
    def create(self, request, *args, **kwargs):
        original_response = super().create(request, *args, **kwargs)
        created_data = original_response.data
        return Response({
            "message": "Record created successfully",
            "data": created_data,
            'success': "true"
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return Response({"message": "Record updated successfully", 'success': "true"}, status=status.HTTP_200_OK)
        # return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"message": "Record deleted successfully",'success': "true"}, status=status.HTTP_204_NO_CONTENT)


def apply_search(queryset, search_fields, search_params):
    """
    Apply search filters to the queryset based on search parameters.
    """
    if search_params:
        for field, value in search_params.items():
            if field in search_fields:
                queryset = queryset.filter(**{f"{field}__icontains": value})
    return queryset


def apply_filters(queryset, filter_params):
    """
    Apply additional filters to the queryset based on filter parameters.
    """
    if filter_params:
        queryset = queryset.filter(**filter_params)
    return queryset


def apply_ordering(queryset, ordering_params):
    """
    Apply ordering to the queryset based on ordering parameters.
    """
    if ordering_params:
        ordering = ordering_params.split(',')
        queryset = queryset.order_by(*ordering)
    return queryset


def paginate_queryset(queryset, start, limit):
    """
    Apply pagination to the queryset based on start and limit parameters.
    """
    return queryset[start:start + limit]


def get_custom_response(queryset, serializer, total_count):
        """
        Formats the custom response for the API.
        """
        if queryset.count() == 0:
            message = 'No records found'
        else:
            message = 'Data fetch successfully'

        return {
            'total_count': total_count,
            'message': message,
            'data': serializer.data,
            'success': "true"

        }


class CustomListAllMixin:
    @action(detail=False, methods=['post'], url_path='get_all_data', permission_classes=[permissions.IsAuthenticated, IsAPIKEYAuthenticated])
    def get_all_data(self, request):
        start = int(request.data.get('start', 0))
        limit = int(request.data.get('limit', 20))
        search_params = request.data.get('search', None)
        filter_params = request.data.get('filters', None)
        ordering_params = request.data.get('ordering', None)

        queryset = self.get_queryset()

        if filter_params:
            queryset = apply_filters(queryset, filter_params)

        if ordering_params:
            queryset = apply_ordering(queryset, ordering_params)

        total_count = queryset.count()

        if search_params:
            queryset = apply_search(queryset, self.search_fields, search_params)

        queryset = paginate_queryset(queryset, start, limit)

        serializer = self.get_serializer(queryset, many=True)
        response_data = get_custom_response(queryset, serializer, total_count)
        return Response(response_data)


class CustomRetrieveMixin:
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsAPIKEYAuthenticated])
    def get_retrieve_data(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # return Response({"message": "Record fetch successfully", 'success': "true"}, status=status.HTTP_201_CREATED)
        data = {
            "message": "Record fetch successfully",
            "data": serializer.data,
            "success": "true"
        }
        return Response(data)


class CustomUpdateMixin:
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsAPIKEYAuthenticated])
    def patch_data(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Record updated successfully", 'success': "true"}, status=status.HTTP_200_OK)
            # return Response(serializer.data)

        return Response({'errors': serializer.errors, 'success': 'false'}, status=400)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsAPIKEYAuthenticated])
    def patch_nested_data(self, request, pk=None):
        instance = self.get_object()
        # request.data.pop('order_items_details')
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Record updated successfully", 'success': "true"}, status=status.HTTP_200_OK)
            # return Response(serializer.data)

        return Response({'errors': serializer.errors, 'success': 'false'}, status=400)


class CustomDeleteMixin:
    @action(detail=True, methods=['post'])
    def delete_data(self, request, pk=None):
        instance = self.get_object()
        try:
            instance.delete()
        except Exception as e:
            raise ValidationError('Unable to delete this record because it is being used in other records.')
        return Response({"message": "Record deleted successfully", 'success': "true"}, status=status.HTTP_200_OK)