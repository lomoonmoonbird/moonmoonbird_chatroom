#--*-- coding: utf-8 --*--

from enum import Enum  # Needs package enum34
from enum import unique


@unique
class ErrorCodes(Enum):
    Ok = 0
    UserPasswordNotMatch = 1
    UserEmailNotExist = 2
    UserPwdEmpty = 3
    UserEmailEmpty = 4
    UserExist = 5
    NotLogin = 6
    JWTokenError = 7
    WebSocketDuplicateConn = 8


    Forbidden = 0xFFFFFFFE
    DeviceHasBeenBanned = 0xFFFFFFFF
    BadRequest = 0x80000000
    InternalServerError = 0x7FFFFFFF
