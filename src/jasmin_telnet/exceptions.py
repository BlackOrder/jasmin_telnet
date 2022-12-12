
class MultiValueDictKeyError(Exception):
    def __init__(self, message="Missing Key in dict"):
        self.message = message
        super().__init__(self.message)


class TelnetUnexpectedResponse(Exception):
    def __init__(self, message="Unexpected response from Jasmin"):
        self.message = message
        super().__init__(self.message)


class TelnetConnectionTimeout(Exception):
    def __init__(self, message="Connection to jcli timed out"):
        self.message = message
        super().__init__(self.message)


class TelnetLoginFailed(Exception):
    def __init__(self, message="Jasmin login failed"):
        self.message = message
        super().__init__(self.message)


class CanNotModifyError(Exception):
    def __init__(self, message="Can not modify a key"):
        self.message = message
        super().__init__(self.message)


class JasminSyntaxError(Exception):
    def __init__(self, message="Can not modify a key"):
        self.message = message
        super().__init__(self.message)


class JasminError(Exception):
    def __init__(self, message="Jasmin error"):
        self.message = message
        super().__init__(self.message)


class UnknownError(Exception):
    def __init__(self, message="object not known"):
        self.message = message
        super().__init__(self.message)


class MissingKeyError(Exception):
    def __init__(self, message="A mandatory key is missing"):
        self.message = message
        super().__init__(self.message)


class MutipleValuesRequiredKeyError(Exception):
    def __init__(self, message="Multiple values are required fro this key"):
        self.message = message
        super().__init__(self.message)


class ActionFailed(Exception):
    def __init__(self, message="Action failed"):
        self.message = message
        super().__init__(self.message)


class ObjectNotFoundError(Exception):
    def __init__(self, message="Object not found"):
        self.message = message
        super().__init__(self.message)
