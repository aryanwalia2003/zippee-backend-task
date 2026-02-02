from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .schemas import RegisterSchema, LoginSchema
from .services import AuthService
from core.decorators import validate_schema
from core.api_utils import ApiResponse, ApiError

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'email', 'password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING, format='email'),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
    responses={201: 'User registered successfully'}
)
@api_view(['POST'])
@csrf_exempt
@validate_schema(RegisterSchema)
def register(request):
    """
    API endpoint to register a new user.
    """
    if request.method != 'POST':
        raise ApiError('Method not allowed', status_code=405)
    
    data = request.validated_data
    user = AuthService.register_user(data.username, data.email, data.password)
    
    return ApiResponse({
        'message': 'User registered successfully',
        'user': {'id': user['id'], 'username': user['username']}
    }, status=201)

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description="Username or Email"),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
    responses={200: 'Login successful'}
)
@api_view(['POST'])
@csrf_exempt
@validate_schema(LoginSchema)
def login(request):
    """
    API endpoint to log in a user.
    """
    if request.method != 'POST':
        raise ApiError('Method not allowed', status_code=405)
    
    data = request.validated_data
    user, token = AuthService.login_user(data.username, data.password)
    
    return ApiResponse({
        'message': 'Login successful',
        'user': {'id': user['id'], 'username': user['username'], 'email': user['email']},
        'token': token
    })
