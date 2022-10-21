from django.test import TestCase
from django.core.cache import cache

from rest_framework.test import APIClient

from .models import TinyURL

class CreateTinyURLTestCase(TestCase):
    def setUp(self):
        TinyURL.objects.create(alias='tinyurl', long_url='http://www.google1.com')

    def test_case_sensitivity(self):
        '''
        1. Testing alias creation api
        2. Testing redirect url for upper / lower case alias
        '''
        # API Case sensitive creation
        client = APIClient()
        resp = client.post(
            '/api/tinyurl', 
            {'alias': 'TINYURL', 'long_url':'http://www.google2.com'},
            format='json')
        self.assertEqual(resp.status_code, 201)

        # Test lower case
        req = self.client.get('/tinyurl', follow=False)
        self.assertEqual(req.status_code, 302)
        self.assertEqual(req.url, 'http://www.google1.com')

        # Test upper case
        req = self.client.get('/TINYURL', follow=False)
        self.assertEqual(req.status_code, 302)
        self.assertEqual(req.url, 'http://www.google2.com')
    
    def test_duplicate_alias(self):
        '''
        1. Test Create API for duplication of alias
        '''
        client = APIClient()
        resp = client.post(
            '/api/tinyurl', 
            {'alias': 'tinyurl', 'long_url':'http://www.google2.com'},
            format='json')

        self.assertEqual(resp.status_code, 400)

    def test_invalid_long_url(self):
        '''
        1. Test Create API for invalid long_url input
        '''
        client = APIClient()
        resp = client.post(
            '/api/tinyurl', 
            {'alias': 'testurl', 'long_url':'//www.google2.com'},
            format='json')

        self.assertEqual(resp.status_code, 400)

        resp = client.post(
            '/api/tinyurl', 
            {'alias': 'testurl', 'long_url':'helo'},
            format='json')

        self.assertEqual(resp.status_code, 400)
    
    def test_character_count(self):
        '''
        1. Test Create API for alias < 5 characters
        2. Test Create API for alias > 10 characters
        '''
        client = APIClient()
        resp = client.post(
            '/api/tinyurl', 
            {'alias': '1234', 'long_url':'http://www.google.com'},
            format='json')

        self.assertEqual(resp.status_code, 400)

        resp = client.post(
            '/api/tinyurl', 
            {'alias': '12345678901', 'long_url':'http://www.googe.com'},
            format='json')

        self.assertEqual(resp.status_code, 400)

    def test_cache(self):
        '''
        1. Test if caching works
        '''

        client = APIClient()
        resp = client.post(
            '/api/tinyurl', 
            {'alias': 'mytest', 'long_url':'http://www.google.com'},
            format='json')

        # cache should be empty
        self.assertEqual(cache.get('mytest'), None)

        req = self.client.get('/mytest', follow=False)
        # cache should exists
        self.assertEqual(cache.get('mytest'), 'http://www.google.com')