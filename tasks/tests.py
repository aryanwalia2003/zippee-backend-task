from django.test import TestCase, Client
from .models import Task
from authentication.models import User
import json

class BaseApiTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = '/auth/register'
        self.login_url = '/auth/login'
        self.tasks_url = '/tasks'
        
        # Create a default user
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        }
        User.create(**self.user_data)
        
        # Login to get token
        login_resp = self.client.post(
            self.login_url, 
            json.dumps({'username': 'testuser', 'password': 'password123'}), 
            content_type='application/json'
        )
        # Fix: Access token from data envelope
        self.token = login_resp.json()['data']['token']
        self.auth_headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}

class TaskTest(BaseApiTest):
    def test_create_task(self):
        data = {'title': 'New Task', 'description': 'Task Desc'}
        resp = self.client.post(self.tasks_url, json.dumps(data), content_type='application/json', **self.auth_headers)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json()['data']['task']['title'], 'New Task')

    def test_get_tasks_list(self):
        Task.create('Task 1', 'Desc 1', self.user_id())
        Task.create('Task 2', 'Desc 2', self.user_id())
        
        resp = self.client.get(self.tasks_url, **self.auth_headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()['data']['tasks']), 2)

    def test_update_task(self):
        task = Task.create('Old Title', 'Old Desc', self.user_id())
        data = {'task_id': task['id'], 'title': 'New Title', 'description': 'Old Desc'}
        
        resp = self.client.post('/tasks/update', json.dumps(data), content_type='application/json', **self.auth_headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['data']['task']['title'], 'New Title')

    def test_complete_task(self):
        task = Task.create('Task', 'Desc', self.user_id())
        data = {'task_id': task['id'], 'completed': True}
        
        resp = self.client.post('/tasks/complete', json.dumps(data), content_type='application/json', **self.auth_headers)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json()['data']['task']['completed'])

    def test_delete_task(self):
        task = Task.create('Task', 'Desc', self.user_id())
        resp = self.client.delete(f'/tasks/{task["id"]}', **self.auth_headers)
        self.assertEqual(resp.status_code, 204)
        
        # Verify gone
        resp_get = self.client.get(f'/tasks/{task["id"]}', **self.auth_headers)
        self.assertEqual(resp_get.status_code, 404)

    def user_id(self):
        # Helper to get current user id from DB
        return User.get_by_username(self.user_data['username'])['id']

class RBACTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Create Admin
        self.admin = User.create('admin', 'admin@example.com', 'pass', role='admin')
        # Create User
        self.user = User.create('user', 'user@example.com', 'pass', role='user')
        
        # Get Admin Token
        resp = self.client.post('/auth/login', json.dumps({'username': 'admin', 'password': 'pass'}), content_type='application/json')
        self.admin_token = resp.json()['data']['token']
        self.admin_headers = {'HTTP_AUTHORIZATION': f'Bearer {self.admin_token}'}

    def test_admin_sees_all_tasks(self):
        # Create tasks for both
        Task.create('Admin Task', 'Desc', self.admin['id'])
        Task.create('User Task', 'Desc', self.user['id'])
        
        resp = self.client.get('/tasks', **self.admin_headers)
        self.assertEqual(resp.status_code, 200)
        # Admin should see 2 tasks
        self.assertEqual(len(resp.json()['data']['tasks']), 2)

    def test_user_sees_only_own_tasks(self):
        # Get User Token
        resp = self.client.post('/auth/login', json.dumps({'username': 'user', 'password': 'pass'}), content_type='application/json')
        user_token = resp.json()['data']['token']
        user_headers = {'HTTP_AUTHORIZATION': f'Bearer {user_token}'}

        Task.create('Admin Task', 'Desc', self.admin['id'])
        Task.create('User Task', 'Desc', self.user['id'])

        resp = self.client.get('/tasks', **user_headers)
        self.assertEqual(resp.status_code, 200)
        # User should see 1 task
        self.assertEqual(len(resp.json()['data']['tasks']), 1)
        self.assertEqual(resp.json()['data']['tasks'][0]['title'], 'User Task')
