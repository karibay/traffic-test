class BaseCheckupException(Exception):
    pass


class AmountNotInRangeException(BaseCheckupException):
    pass


class AgeNotInRangeException(BaseCheckupException):
    pass


class UserIsIEException(BaseCheckupException):
    pass


class UserIsBlackListedException(BaseCheckupException):
    pass
