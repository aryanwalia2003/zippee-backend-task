from core.api_utils import ApiResponse, ApiError
import traceback

class GlobalExceptionHandlerMiddleware:
    """
    Middleware to handle global exceptions and return standardized JSON responses.
    """
    def __init__(self, get_response):
        """
        Initialize the middleware.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Process the request.
        """
        return self.get_response(request)

    def process_exception(self, request, exception):
        """
        Handle exceptions raised during request processing.
        """
        if isinstance(exception, ApiError):
            return ApiResponse(
                success=False,
                message=exception.message,
                data=exception.data,
                status=exception.status_code
            )
        
        print(traceback.format_exc())
        
        return ApiResponse(
            success=False,
            message="Internal Server Error",
            status=500
        )
