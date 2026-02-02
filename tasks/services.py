from .models import Task
from core.utils import encode_cursor, decode_cursor
from core.api_utils import NotFoundError, UnauthorizedError

class TaskService:
    """
    Service class for handling task-related logic.
    """
    @staticmethod
    def get_task_list(user_id, role, limit, cursor_str, direction, status_param, sort_order):
        """
        Retrieve a paginated list of tasks.
        """
        cursor_id = decode_cursor(cursor_str)
        
        try:
            limit = int(limit)
        except (ValueError, TypeError):
            limit = 10

        status = None
        if status_param is not None:
            if status_param.lower() == 'true':
                status = True
            elif status_param.lower() == 'false':
                status = False

        tasks = Task.get_list(user_id, role, limit, cursor_id, direction, status, sort_order)
        
        has_more = False
        if len(tasks) > limit:
            has_more = True
            tasks.pop() 
            
        next_cursor = None
        prev_cursor = None
        
        if tasks:
            if has_more:
                next_cursor = encode_cursor(tasks[-1]['id'])
            if cursor_id:
                prev_cursor = encode_cursor(tasks[0]['id']) 
                
        return tasks, prev_cursor, next_cursor

    @staticmethod
    def get_task_detail(user_id, task_id):
        """
        Retrieve details of a specific task.
        """
        task = Task.get_by_id(task_id)
        if not task:
            raise NotFoundError('Task not found')
            
        if task['user_id'] != user_id: 
             user_role = 'user' 
             if user_role != 'admin': 
                raise UnauthorizedError('Not authorized to access this task')
        
        return task

    @staticmethod
    def create_task(user_id, title, description):
        """
        Create a new task.
        """
        return Task.create(title, description, user_id)

    @staticmethod
    def update_task(user_id, task_id, title=None, description=None):
        """
        Update an existing task.
        """
        task = Task.get_by_id(task_id)
        if not task:
            raise NotFoundError('Task not found')
            
        if task['user_id'] != user_id:
            raise UnauthorizedError('Not authorized to update this task')
            
        updated_task = Task.update(task_id, title=title, description=description)
        return updated_task

    @staticmethod
    def complete_task(user_id, task_id, completed):
        """
        Mark a task as completed or incomplete.
        """
        task = Task.get_by_id(task_id)
        if not task:
            raise NotFoundError('Task not found')
            
        if task['user_id'] != user_id:
            raise UnauthorizedError('Not authorized to update this task')
            
        updated_task = Task.update(task_id, completed=completed)
        return updated_task

    @staticmethod
    def delete_task(user_id, task_id):
        """
        Delete a task.
        """
        task = Task.get_by_id(task_id)
        if not task:
             raise NotFoundError('Task not found')
             
        if task['user_id'] != user_id:
            raise UnauthorizedError('Not authorized to delete this task')
            
        Task.delete(task_id)
