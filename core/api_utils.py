class ApiError(Exception):
    """
    Custom exception class for API errors.
    """
    def __init__(self, message, data=None, status_code=400):
        """
        Initialize the ApiError.
        """
        super().__init__(message)
        self.message = message
        self.data = data
        self.status_code = status_code

class ValidationError(ApiError):
    """
    Exception raised for validation errors.
    """
    def __init__(self, message, data=None):
        """
        Initialize the ValidationError.
        """
        super().__init__(message, data=data, status_code=422)

class UnauthorizedError(ApiError):
    """
    Exception raised for unauthorized access.
    """
    def __init__(self, message="Unauthorized"):
        """
        Initialize the UnauthorizedError.
        """
        super().__init__(message, status_code=401)

class NotFoundError(ApiError):
    """
    Exception raised when a resource is not found.
    """
    def __init__(self, message="Not Found"):
        """
        Initialize the NotFoundError.
        """
        super().__init__(message, status_code=404)

from django.http import JsonResponse

def ApiResponse(data=None, success=True, message=None, status=200):
    """
    Helper function to create a standardized JSON response.
    """
    response_data = {
        "success": success,
        "status": status,
        "data": data,
        "message": message
    }
    return JsonResponse(response_data, status=status)
