from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PaginationHousings(PageNumberPagination):
    page_size = 10
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'result': data
        })



