from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'Всего': self.page.paginator.count,
            'Следующая': self.get_next_link(),
            'Предыдущая': self.get_previous_link(),
            'Результаты': data,
        })