from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APIClient

from geosite.sysinfo.models import Request
from geosite.sysinfo.utilities import get_req_type_from_rest_verb

from .models import Request


class RequestsTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a test user
        user = User.objects.create_user(username='username',
                                        email='test@test.com',
                                        password='password')

        self.client = APIClient()
        self.client.login(username='username', password='password')

        # Create 10 entries
        for _ in range(0, 10):
            ret = self.client.get('')
            self.assertEqual(ret.status_code, 200)

    def test_non_existent_entry(self):
        ret = self.client.get('/api/44/')
        self.assertEqual(ret.status_code, 404)

    def test_entry_that_exists(self):
        ret = self.client.get('/api/1/')
        self.assertEqual(ret.status_code, 200)

    def test_put(self):
        ret = self.client.put('/api/1/')
        self.assertEqual(ret.status_code, 405)

    def test_delete_existing(self):
        ret = self.client.delete('/api/1/')
        self.assertEqual(ret.status_code, 200)

        ret = self.client.get('/api/1/')
        self.assertEqual(ret.status_code, 404)

    def test_delete_non_existing(self):
        ret = self.client.delete('/api/20/')
        self.assertEqual(ret.status_code, 400)

    def test_update_comment(self):
        ret = self.client.post('/api/7/', {"comment": "test_comment"})
        self.assertEqual(ret.status_code, 200)

        entry = Request.objects.get(id="7")
        self.assertEqual(entry.comment, "test_comment")

    def test_update_comment_with_req_type(self):
        ret = self.client.post('/api/7/', {"comment": "test_comment", "req_type": 1})
        self.assertEqual(ret.status_code, 200)

        entry = Request.objects.get(id="7")
        self.assertEqual(entry.comment, "test_comment")

        # Make sure that a POST cannot be used to change the req_type, only the comment
        self.assertEqual(entry.req_type, get_req_type_from_rest_verb("GET"))
