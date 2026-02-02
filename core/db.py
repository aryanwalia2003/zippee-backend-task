from django.db import connection

def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    """
    Execute a raw SQL query on the database.
    """
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        if fetch_one:
            columns = [col[0] for col in cursor.description]
            row = cursor.fetchone()
            if row:
                return dict(zip(columns, row))
            return None
        if fetch_all:
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]
        return None
