"""Infobús client exceptions."""

from typing import Optional


class InfobusError(Exception):
    """Base exception for all Infobús client errors."""
    
    def __init__(self, message: str) -> None:
        """Initialize the exception with a message.
        
        Args:
            message: Error message
        """
        self.message = message
        super().__init__(message)


class InfobusConnectionError(InfobusError):
    """Exception raised for connection-related errors."""
    
    def __init__(self, message: str) -> None:
        """Initialize the connection error.
        
        Args:
            message: Error message describing the connection issue
        """
        super().__init__(f"Connection error: {message}")


class InfobusAPIError(InfobusError):
    """Exception raised for API-related errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None) -> None:
        """Initialize the API error.
        
        Args:
            message: Error message from the API
            status_code: HTTP status code if available
        """
        self.status_code = status_code
        if status_code:
            super().__init__(f"API error ({status_code}): {message}")
        else:
            super().__init__(f"API error: {message}")


class InfobusValidationError(InfobusError):
    """Exception raised for data validation errors."""
    
    def __init__(self, message: str, field: Optional[str] = None) -> None:
        """Initialize the validation error.
        
        Args:
            message: Error message describing the validation issue
            field: Field name that failed validation (if applicable)
        """
        self.field = field
        if field:
            super().__init__(f"Validation error in '{field}': {message}")
        else:
            super().__init__(f"Validation error: {message}")


class InfobusAuthenticationError(InfobusAPIError):
    """Exception raised for authentication-related errors."""
    
    def __init__(self, message: str = "Authentication failed") -> None:
        """Initialize the authentication error.
        
        Args:
            message: Error message
        """
        super().__init__(message, status_code=401)


class InfobusRateLimitError(InfobusAPIError):
    """Exception raised when API rate limits are exceeded."""
    
    def __init__(self, message: str = "Rate limit exceeded") -> None:
        """Initialize the rate limit error.
        
        Args:
            message: Error message
        """
        super().__init__(message, status_code=429)
