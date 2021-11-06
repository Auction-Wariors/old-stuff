
from django.test import TestCase

from django.contrib.auth import get_user_model
from app.stores.models import Store

# Create your tests here.

User = get_user_model()
Store = Store.objects.create()


class TestStoresForms(TestCase):

    # Setup for the stores\tests to run.
    def setUp(self):
        user_a_password = 'testUserA'
        self.user_a = User(username='testUserA', email='TestUserA@notemail.com', password=user_a_password)
        self.store_a = Store(name='testStoreA', owner='user_a')

    # Verifying that setup was completed, and test user created.
    def test_verify_test_setup(self):

        # Test parameters
        user_qs = User.objects.filter(username_iexact='testUserA')
        user_exists = user_qs.exitsts() and user_qs.count == 1
        store_qs = Store.objects.filter(name_iexact='testStoreA')
        store_exists = store_qs.exitsts() and store_qs.count == 1
        user_a = user_qs.first()

        # User checks
        self.assertTrue(user_exists)
        self.assertNotEqual(user_exists.count(), 0)
        self.assertTrue(user_a.check_password('testUserA'))

        # Store checks
        self.assertTrue(store_exists)
        self.assertNotEqual(store_exists.count(), 0)
        self.assertTrue(self.store_a.owner(self.user_a))

    def test_register_store_only_when_logged_in(self):
        pass
