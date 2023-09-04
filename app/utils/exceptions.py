from app.utils.error_codes import ErrorCodes


class AppException(Exception):
    def __init__(self, error_code, message=''):
        self.code = error_code
        self.message = message


class RequestParamError(AppException):
    def __init__(self, message):
        super(RequestParamError, self).__init__(ErrorCodes.BadRequest, message)


class ForbiddenError(AppException):
    def __init__(self, message):
        super(ForbiddenError, self).__init__(ErrorCodes.Forbidden, message)


class CacheHit(AppException):
    def __init__(self, data):
        self.code = ErrorCodes.Ok
        self.message = ''
        self.data = data

"""
authentication exception
"""

class UserPasswordNotMatchError(AppException):
    def __init__(self, message):
        super(UserPasswordNotMatchError, self).__init__(ErrorCodes.UserPasswordNotMatch, message)

class UserNotExistError(AppException):
    def __init__(self, message):
        super(UserNotExistError, self).__init__(ErrorCodes.UserEmailNotExist, message)

class UserEmailEmptyError(AppException):
    def __init__(self, message):
        super(UserEmailEmptyError, self).__init__(ErrorCodes.UserEmailEmpty, message)

class UserPwdEmptyError(AppException):
    def __init__(self, message):
        super(UserPwdEmptyError, self).__init__(ErrorCodes.UserPwdEmpty, message)

class UserExistError(AppException):
    def __init__(self, message):
        super(UserExistError, self).__init__(ErrorCodes.UserExist, message)

class JWTokenError(AppException):
    def __init__(self, message):
        super(JWTokenError, self).__init__(ErrorCodes.JWTokenError, message)

"""
websocket 
"""
class DuplicateConnError(AppException):
    def __init__(self, message):
        super(DuplicateConnError, self).__init__(ErrorCodes.WebSocketDuplicateConn, message)