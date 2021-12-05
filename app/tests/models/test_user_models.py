from django.test import TestCase
from django.contrib.auth import get_user_model

from users.models import Profile

User = get_user_model()


class UserModelTestClass(TestCase):
    """Testing the user model"""
    @classmethod
    def setUpTestData(cls):
        """setUpTestData: Run once to set up non-modified data for all class methods."""
        User.objects.create(username='test', password='test')

    def test_user_stored_in_db(self):
        self.assertEqual(User.objects.get(username='test').username, 'test')

    def test_creating_user_creates_profile_signals(self):
        user = User.objects.get(username='test')
        profile = Profile.objects.get(user=user)

        self.assertEqual(user.id, profile.user.id)


class UserProfileModelTestClass(TestCase):
    """Testing the user profile model"""
    @classmethod
    def setUpTestData(cls):
        """setUpTestData: Run once to set up non-modified data for all class methods."""
        # User creating also creates profile through Django Signals
        user = User.objects.create(username='test_user', password='test_password')

        cls.user = user
        profile: Profile = user.profile

        # Populating user profile
        profile.phone_number = '555-555-555'
        profile.street_address = 'test address 1'
        profile.city = 'test city'
        profile.zip_code = '5555'
        profile.save()

    def test_user_profile_fields_label(self):
        profile = self.user.profile

        self.assertEqual(profile._meta.get_field('user').verbose_name, 'user')
        self.assertEqual(profile._meta.get_field('phone_number').verbose_name, 'phone number')
        self.assertEqual(profile._meta.get_field('street_address').verbose_name, 'street address')
        self.assertEqual(profile._meta.get_field('city').verbose_name, 'city')
        self.assertEqual(profile._meta.get_field('zip_code').verbose_name, 'zip code')

    def test_user_profile_fields_max_length(self):
        profile = self.user.profile

        self.assertEqual(profile._meta.get_field('phone_number').max_length, 12)
        self.assertEqual(profile._meta.get_field('street_address').max_length, 100)
        self.assertEqual(profile._meta.get_field('city').max_length, 100)
        self.assertEqual(profile._meta.get_field('zip_code').max_length, 5)

    def test_user_profile_fields_default_value(self):
        profile = self.user.profile

        self.assertEqual(profile._meta.get_field('phone_number').default, '')
        self.assertEqual(profile._meta.get_field('street_address').default, '')
        self.assertEqual(profile._meta.get_field('city').default, '')
        self.assertEqual(profile._meta.get_field('zip_code').default, '')

    def test_user_profile_model__str__(self):
        profile = self.user.profile

        expected_object_name = f"{self.user.username}'s Profile"
        self.assertEqual(expected_object_name, str(profile))

