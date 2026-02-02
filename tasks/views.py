from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .schemas import TaskCreateSchema, TaskUpdateSchema, TaskCompleteSchema
from authentication.utils import login_required
from core.decorators import validate_schema
from core.api_utils import ApiResponse
from .services import TaskService

@api_view(['GET', 'POST'])
@csrf_exempt
@login_required
@validate_schema(TaskCreateSchema)
def task_list(request):
    """
    API endpoint to list tasks or create a new task.
    """
    if request.method == 'GET':
        tasks, prev, next_c = TaskService.get_task_list(
            user_id=request.user_id,
            role=getattr(request, 'role', 'user'),
            limit=request.GET.get('limit', 10),
            cursor_str=request.GET.get('cursor'),
            direction=request.GET.get('direction', 'next'),
            status_param=request.GET.get('status'),
            sort_order=request.GET.get('sort_order', 'desc')
        )
        
        return ApiResponse({
            'tasks': tasks,
            'prev_cursor': prev,
            'next_cursor': next_c
        })
    
    elif request.method == 'POST':
        data = request.validated_data
        task = TaskService.create_task(request.user_id, data.title, data.description)
        return ApiResponse({'message': 'Task created', 'task': task}, status=201)

@api_view(['GET', 'DELETE'])
@csrf_exempt
@login_required
def task_detail(request, task_id):
    """
    API endpoint to retrieve or delete a specific task.
    """
    if request.method == 'GET':
        task = TaskService.get_task_detail(request.user_id, task_id)
        return ApiResponse({'task': task})

    elif request.method == 'DELETE':
        TaskService.delete_task(request.user_id, task_id)
        return ApiResponse({'message': 'Task deleted'}, status=204)

@api_view(['POST'])
@csrf_exempt
@login_required
@validate_schema(TaskUpdateSchema)
def update_task(request):
    """
    API endpoint to update a task's details.
    """
    data = request.validated_data
    updated_task = TaskService.update_task(
        request.user_id, 
        data.task_id, 
        title=data.title, 
        description=data.description
    )
    return ApiResponse({'message': 'Task updated', 'task': updated_task})

@api_view(['POST'])
@csrf_exempt
@login_required
@validate_schema(TaskCompleteSchema)
def complete_task(request):
    """
    API endpoint to mark a task as completed or incomplete.
    """
    data = request.validated_data
    updated_task = TaskService.complete_task(request.user_id, data.task_id, data.completed)
    return ApiResponse({'message': 'Task status updated', 'task': updated_task})
