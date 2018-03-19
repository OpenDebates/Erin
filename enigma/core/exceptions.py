class EnigmaCoreException(Exception):
    """Base exception class for Core modules and internal use"""
    pass


class EnigmaUserException(Exception):
    """Base exception class raised as a byproduct of misconfiguration"""
    pass


class EnigmaPluginException(Exception):
    """Base exception class for plugin errors"""
    pass


class EnigmaEnvironmentVariableError(EnigmaUserException):
    """
    Error raised when an environment variable is not configured
    properly.
    """
    def __init__(self, message):
        self.message = message
