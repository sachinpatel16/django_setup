from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'page': self.page.number,
            'page_size': len(self.page.object_list),
            'total_count': self.page.paginator.count,
            'results': data
        })
