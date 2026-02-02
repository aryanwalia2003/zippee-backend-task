import json
from functools import wraps
from pydantic import ValidationError as PydanticValidationError
from core.api_utils import ValidationError

def validate_schema(schema_class):
    """
    Decorator to validate request body against a Pydantic schema.
    """
    def decorator(f):
        """
        The actual decorator wrapper.
        """
        @wraps(f)
        def decorated_function(request, *args, **kwargs):
            """
            The wrapped view function that performs validation.
            """
            try:
                if request.method in ['POST', 'PUT', 'PATCH']:
                    try:
                        data = json.loads(request.body)
                    except json.JSONDecodeError:
                        raise ValidationError("Invalid JSON body")
                    
                    validated_data = schema_class(**data)
                    request.validated_data = validated_data
            except PydanticValidationError as e:
                errors = []
                for error in e.errors():
                    field = ".".join(str(x) for x in error['loc'])
                    msg = error['msg']
                    errors.append(f"{field}: {msg}")
                raise ValidationError("Validation Failed", data=errors)
                
            return f(request, *args, **kwargs)
        return decorated_function
    return decorator
