from django.test import TestCase
from django.contrib.auth import get_user_model

from stores.models import Store

User = get_user_model()


class StoreModelInitialTestClass(TestCase):
    """Initial tests"""

    @classmethod
    def setUpTestData(cls):
        """setUpTestData: Run once to set up non-modified data for all class methods."""
        cls.user = User.objects.create(username='test', password='test')

    def test_that_user_can_create_a_store(self):
        store = Store.objects.create(name='test store',
                                     owner=self.user,
                                     description='test store description',
                                     email='test@teststore.com',
                                     phone_number='555 555 555')

        self.assertEqual(Store.objects.get(pk=1), store)


class StoreModelTestClass(TestCase):
    """Testing the Stores models"""

    @classmethod
    def setUpTestData(cls):
        """setUpTestData: Run once to set up non-modified data for all class methods."""
        user = User.objects.create(username='test', password='test')

        cls.user = user
        cls.store = Store.objects.create(name='test store',
                                         owner=user,
                                         description='test store description',
                                         email='test@teststore.com',
                                         phone_number='555 555 555')

    def test_store_fields_label(self):
        self.assertEqual(self.store._meta.get_field('name').verbose_name, 'name')
        self.assertEqual(self.store._meta.get_field('owner').verbose_name, 'owner')
        self.assertEqual(self.store._meta.get_field('description').verbose_name, 'description')
        self.assertEqual(self.store._meta.get_field('email').verbose_name, 'email')
        self.assertEqual(self.store._meta.get_field('phone_number').verbose_name, 'phone number')

    def test_store_fields_max_length(self):
        self.assertEqual(self.store._meta.get_field('name').max_length, 100)
        self.assertEqual(self.store._meta.get_field('description').max_length, 1000)
        self.assertEqual(self.store._meta.get_field('phone_number').max_length, 12)

    def test_store_model__str__(self):
        self.assertEqual(self.store.name, str(self.store))
