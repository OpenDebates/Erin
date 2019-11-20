class CoreError(Exception):
    """Base exception class for Core modules and internal use"""

    pass


class UserError(Exception):
    """Base exception class raised as a byproduct of misconfiguration"""

    pass


class PluginError(Exception):
    """Base exception class for plugin errors"""

    pass


class PluginNotFoundError(PluginError, FileNotFoundError):
    """
    Raised when a plugin path is requested but doesn’t exist.
    Corresponds to errno `ENOENT`.
    """

    def __init__(self, path, message=None):
        if not message:
            message = f"[Errno 2] No such path: '{path}'"
        super().__init__(message)


class EnvironmentVariableError(UserError):
    """
    Error raised when an environment variable is not configured
    properly.
    """

    def __init__(self, message):
        super().__init__(message)


class DatabaseError(CoreError):
    """
    Error raised when a database operation fails.
    """

    pass


class DatabaseKeyError(DatabaseError):
    """
    Raised when an attempt to fetch from the key value store fails.
    """

    def __init__(self, message):
        super().__init__(message)


class PrimaryKeyError(DatabaseError):
    """
    Raised when there is either a primary key is missing or required.
    """

    def __init__(self, message):
        super().__init__(message)


class TableNotFoundError(DatabaseError):
    """
    Raised when a table is missing.
    """

    def __init__(self, message):
        super().__init__(message)


class RecordExistsError(DatabaseError):
    """
    Raised when a record already exists.
    """

    def __init__(self, message):
        super().__init__(message)


class DatabaseTypeError(DatabaseError):
    """
    Raised when parameters passed are incorrect.
    """

    def __init__(self, message):
        super().__init__(message)
