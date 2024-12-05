from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    if isinstance(exc, ReasonException):
        return Response({'reason': exc.reason}, status=exc.status_code)

    if (response := exception_handler(exc, context)) is None:
        return response

    return Response({'reason': response.data}, status=response.status_code)


class ReasonException(Exception):
    def __init__(self, reason='Not found', status_code=status.HTTP_404_NOT_FOUND):
        self.reason = reason
        self.status_code = status_code
