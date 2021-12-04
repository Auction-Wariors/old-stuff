from django.contrib.auth.models import User
from django.test import TestCase
from http import HTTPStatus
from django.utils import timezone
from django.urls import reverse

from auctions.models import Category, Auction, Bid
from stores.models import Store


class TestCreateStore(TestCase):
    """Testing update auction view"""

    @classmethod
    def setUpTestData(cls):
        """ Set up test data for update auction"""
        user = User.objects.create(username='test_user')
        user.set_password('test123')
        user.save()

    def test_create_store_success(self):
        self.client.login(username='test_user', password='test123')

        response = self.client.post(reverse('stores:create_store'), data={'name': 'Test Store',
                                                                          'description': 'Test Store Description',
                                                                          'email': 'test@teststore.com',
                                                                          'phone_number': '00000000'})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], reverse('stores:store_dashboard'))

    def test_create_store_user_has_store(self):
        user = User.objects.get(username='test_user')
        store = Store.objects.create(name='Test Store',
                                     description='Test Store Description',
                                     email='test@teststore.com',
                                     phone_number='00000000',
                                     owner=user)
        store.save()

        self.client.login(username='test_user', password='test123')

        response = self.client.get(reverse('stores:create_store'), follow=True)
        self.assertRedirects(response, reverse('stores:store_dashboard'),
                             status_code=302,
                             target_status_code=200)

    def test_create_store_get(self):
        self.client.login(username='test_user', password='test123')

        response = self.client.get(reverse('stores:create_store'), follow=True)
        self.assertTemplateUsed(response, 'stores/create_store.html')
        self.assertContains(response, 'Register your Store', html=True)