

class ExceptionBase(Exception):
    """Base exception class for authentication errors."""
    pass


class InsufficientPermissions(ExceptionBase):
    """Exception raised when a user lacks necessary permissions."""
    def __init__(self, message="User does not have sufficient permissions."):
        self.message = message
        super().__init__(self.message)


class AccountNotVerified(ExceptionBase):
    """Exception raised when a user's account is not verified."""
    def __init__(self, message="User account is not verified."):
        self.message = message
        super().__init__(self.message)
        
