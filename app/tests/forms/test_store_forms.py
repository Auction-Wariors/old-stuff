from django.test import TestCase


from django.contrib.auth.models import User
from stores.forms import CreateStoreForm
from stores.models import Store


class TestCreateStoreForm(TestCase):

    def setUp(self):
        """ Set up test data for create store form"""
        self.user_1 = User.objects.create(username='test', password='test123')
        user2 = User.objects.create(username='test2', password='test123')
        Store.objects.create(name='Store', description='Test', email='email@store.com', phone_number='45678910', owner=user2)

    def test_create_store_form_is_valid(self):
        form = CreateStoreForm(data={
            'name': 'Store 1',
            'description': 'Test',
            'email': 'test@store.com',
            'phone_number': '99999999',
        })

        self.assertTrue(form.is_valid())

    def test_create_store_form_store_name_already_exists(self):
        form = CreateStoreForm(data={
            'name': 'Store',
            'description': 'Test',
            'email': 'test@store.com',
            'phone_number': '99999999',
        })

        self.assertEqual(len(form.errors), 1)

    def test_create_store_form_is_not_valid(self):
        form = CreateStoreForm(data={
            'name': 'Store 1',
            'description': 'Test',
        })

        self.assertEqual(len(form.errors), 2)



