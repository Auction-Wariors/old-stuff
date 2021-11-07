
from django.test import TestCase

from django.contrib.auth import get_user_model
from stores.models import Store

# Create your tests here.
from stores.forms import CreateStoreForm

User = get_user_model()

# Testing stores.forms.py

class TestStoresForms(TestCase):

    def setUp(self):
        user_password = 'testPassword'
        user_owner = User.objects.create(username="user_owner", password=user_password)

        store_name = "test store"
        store = Store.objects.create(name=store_name, owner=user_owner, description='hello',
                                     email='not@email.com', phone_number='11112222')

    def test_create_valid_store(self):

        # Setting test variables
        full_form = CreateStoreForm(data={'name': 'test store 1',
                                          'description': 'lorem ipsum',
                                          'email': 'isnot@email.com',
                                          'phone_number': '22223333'})
        not_complete_form = CreateStoreForm(data={'name': '',
                                          'description': 'lorem ipsum',
                                          'email': 'isnot@email.com',
                                          'phone_number': ''})
        empty_form = CreateStoreForm(data={'name': '',
                                          'description': '',
                                          'email': '',
                                          'phone_number': ''})
        no_name_in_form = CreateStoreForm(data={'name': '',
                                          'description': 'lorem ipsum',
                                          'email': 'isnot@email.com',
                                          'phone_number': '22223333'})
        no_description_in_form = CreateStoreForm(data={'name': 'test store 1',
                                          'description': '',
                                          'email': 'isnot@email.com',
                                          'phone_number': '22223333'})
        no_email_in_form = CreateStoreForm(data={'name': 'test store 1',
                                          'description': 'lorem ipsum',
                                          'email': '',
                                          'phone_number': '22223333'})
        no_phone_number_in_form = CreateStoreForm(data={'name': 'test store 1',
                                          'description': 'lorem ipsum',
                                          'email': 'isnot@email.com',
                                          'phone_number': ''})
        wrong_format_email_in_form = CreateStoreForm(data={'name': 'test store 1',
                                          'description': 'lorem ipsum',
                                          'email': '123151423',
                                          'phone_number': 'notPhoneNo'})

        # Checking the different forms
        self.assertTrue(full_form.is_valid())
        self.assertEqual(len(empty_form.errors), 4)
        self.assertFalse(not_complete_form.is_valid())
        self.assertFalse(no_name_in_form.is_valid())
        self.assertFalse(no_description_in_form.is_valid())
        self.assertFalse(no_email_in_form.is_valid())
        self.assertFalse(no_phone_number_in_form.is_valid())
        self.assertFalse(wrong_format_email_in_form.is_valid())

