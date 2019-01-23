class CoreError(Exception):
    """Base exception class for Core modules and internal use"""
    pass


class UserError(Exception):
    """Base exception class raised as a byproduct of misconfiguration"""
    pass


class PluginError(Exception):
    """Base exception class for plugin errors"""
    pass


class EnvironmentVariableError(UserError):
    """
    Error raised when an environment variable is not configured
    properly.
    """
    def __init__(self, message):
        self.message = message


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
        self.message = message


class PrimaryKeyError(DatabaseError):
    """
    Raised when there is either a primary key is missing or required.
    """
    def __init__(self, message):
        self.message = message


class TableNotFoundError(DatabaseError):
    """
    Raised when a table is missing.
    """
    def __init__(self, message):
        self.message = message


class RecordExistsError(DatabaseError):
    """
    Raised when a record already exists.
    """
    def __init__(self, message):
        self.message = message


class DatabaseTypeError(DatabaseError):
    """
    Raised when parameters passed are incorrect.
    """
    def __init__(self, message):
        self.message = message
