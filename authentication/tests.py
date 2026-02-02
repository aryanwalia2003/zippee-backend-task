from django.test import TestCase, Client
from .models import User
import json

class AuthTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_success(self):
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'password123'
        }
        resp = self.client.post('/auth/register', json.dumps(data), content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        # Check data envelope
        self.assertIn('user', resp.json()['data'])

    def test_register_duplicate(self):
        User.create('dupuser', 'dup@example.com', 'pass')
        data = {
            'username': 'dupuser',
            'email': 'other@example.com',
            'password': 'pass'
        }
        resp = self.client.post('/auth/register', json.dumps(data), content_type='application/json')
        # Expect 422 for ValidationError
        self.assertEqual(resp.status_code, 422)

    def test_login_success(self):
        User.create('loginuser', 'login@example.com', 'pass')
        data = {'username': 'loginuser', 'password': 'pass'}
        resp = self.client.post('/auth/login', json.dumps(data), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('token', resp.json()['data'])

    def test_login_invalid(self):
        data = {'username': 'wrong', 'password': 'wrong'}
        resp = self.client.post('/auth/login', json.dumps(data), content_type='application/json')
        self.assertEqual(resp.status_code, 401)
