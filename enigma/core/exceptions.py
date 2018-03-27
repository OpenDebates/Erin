class EnigmaCoreError(Exception):
    """Base exception class for Core modules and internal use"""
    pass


class EnigmaUserError(Exception):
    """Base exception class raised as a byproduct of misconfiguration"""
    pass


class EnigmaPluginError(Exception):
    """Base exception class for plugin errors"""
    pass


class EnigmaEnvironmentVariableError(EnigmaUserError):
    """
    Error raised when an environment variable is not configured
    properly.
    """
    def __init__(self, message):
        self.message = message


class EnigmaDatabaseError(EnigmaCoreError):
    """
    Error raised when a database operation fails.
    """
    def __init__(self, message):
        self.message = message
