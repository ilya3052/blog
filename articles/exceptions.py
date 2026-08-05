from rest_framework.exceptions import APIException


class UserNotFoundError(APIException):
    status_code = 404
    default_detail = 'Пользователь с таким username не найден'