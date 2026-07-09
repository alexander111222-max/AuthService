class AuthSystemException(Exception):
    detail = "Произошла непредвиденная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class TokenExpiredError(AuthSystemException):
    detail = "Токен истёк"


class InvalidTokenError(AuthSystemException):
    detail = "Невалидный токен"


class MultipleResultsFoundException(AuthSystemException):
    detail = "Слишком много объектов"


class NoResultFoundException(AuthSystemException):
    detail = "Не найдено результатов"


class ObjectAlreadyExistsException(AuthSystemException):
    detail = "Объект уже существует"


# Users
class UserNotFoundException(AuthSystemException):
    detail = "Пользователь не найден"


class UserAlreadyExistsException(AuthSystemException):
    detail = "Пользователь с таким email уже существует"


class UserNotActiveException(AuthSystemException):
    detail = "Аккаунт деактивирован"


class WrongPasswordException(AuthSystemException):
    detail = "Неверный пароль"


# Roles
class RoleNotFoundException(AuthSystemException):
    detail = "Роль не найдена"


class RoleAlreadyExistsException(AuthSystemException):
    detail = "Роль уже существует"


# Entities
class EntityNotFoundException(AuthSystemException):
    detail = "Сущность не найдена"


class EntityAlreadyExistsException(AuthSystemException):
    detail = "Сущность уже существует"


# Permissions
class PermissionNotFoundException(AuthSystemException):
    detail = "Право доступа не найдено"


class PermissionAlreadyExistsException(AuthSystemException):
    detail = "Такое право доступа уже существует"


class ForbiddenException(AuthSystemException):
    detail = "Доступ запрещён"


class UnauthorizedException(AuthSystemException):
    detail = "Необходима авторизация"