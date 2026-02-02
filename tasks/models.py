from core.db import execute_query

class Task:
    """
    Model representing a task.
    """
    @staticmethod
    def create(title, description, user_id):
        """
        Create a new task.
        """
        query = """
            INSERT INTO app_tasks (title, description, user_id)
            VALUES (%s, %s, %s)
            RETURNING id, title, description, completed, created_at, user_id;
        """
        return execute_query(query, (title, description, user_id), fetch_one=True)

    @staticmethod
    def get_by_id(task_id):
        """
        Retrieve a task by its ID.
        """
        query = "SELECT * FROM app_tasks WHERE id = %s;"
        return execute_query(query, (task_id,), fetch_one=True)

    @staticmethod
    def update(task_id, title=None, description=None, completed=None):
        """
        Update a task's details.
        """
        updates = []
        params = []
        
        if title is not None:
            updates.append("title = %s")
            params.append(title)
            
        if description is not None:
            updates.append("description = %s")
            params.append(description)
            
        if completed is not None:
            updates.append("completed = %s")
            params.append(completed)
            
        if not updates:
            return None
            
        query = f"""
            UPDATE app_tasks
            SET {', '.join(updates)}, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            RETURNING *;
        """
        params.append(task_id)
        
        return execute_query(query, tuple(params), fetch_one=True)

    @staticmethod
    def delete(task_id):
        """
        Delete a task by its ID.
        """
        query = "DELETE FROM app_tasks WHERE id = %s;"
        execute_query(query, (task_id,))

    @staticmethod
    def get_list(user_id, role='user', limit=10, cursor=None, direction='next', status=None, sort_order='desc'):
        """
        Retrieve a list of tasks with pagination and filtering.
        """
        base_query = "SELECT * FROM app_tasks WHERE 1=1"
        params = []
        
        if role != 'admin':
            base_query += " AND user_id = %s"
            params.append(user_id)
            
        if status is not None:
            base_query += " AND completed = %s"
            params.append(status)
            
        if cursor:
            op = '<' if (direction == 'next' and sort_order == 'desc') or (direction == 'prev' and sort_order == 'asc') else '>'
            base_query += f" AND id {op} %s"
            params.append(cursor)
            
        order = 'DESC' if sort_order == 'desc' else 'ASC'
        base_query += f" ORDER BY id {order} LIMIT %s"
        params.append(limit + 1)
        
        tasks = execute_query(base_query, tuple(params), fetch_all=True)
        return tasks
