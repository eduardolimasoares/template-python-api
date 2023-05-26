class InvalidOrUnauthorizedApp(Exception):
    pass


class EmailAndOrPasswordInvalidError(Exception):
    pass


class InvalidTokenType(Exception):
    pass


class MissingAuthenticationHeaderError(Exception):
    pass


class MalformedAuthorizationHeaderError(Exception):
    pass


class EmailIsInvalidOrDontExists(Exception):
    pass