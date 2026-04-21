class InvalidUserException(Exception):
    pass


class InvalidPostException(Exception):
    pass


class InvalidCommentException(Exception):
    pass


class InvalidReactionTypeException(Exception):
    pass


class UserCannotDeletePostException(Exception):
    pass

class InvalidGroupNameException(Exception):
    pass

class InvalidMemberException(Exception):
    pass

class InvalidGroupException(Exception):
    pass

class UserNotInGroupException(Exception):
    pass

class UserNotAdminException(Exception):
    pass


class UserIsNotAdminException(UserNotAdminException):
    pass


class InvalidOffSetValueException(Exception):
    pass


class InvalidLimitSetValueException(Exception):
    pass
