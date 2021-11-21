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

    def test_creating_user_creates_profile_signals(self):
        user = User.objects.get(username='test')
        profile = Profile.objects.get(user=user)

        self.assertEqual(user.id, profile.user.id)


class UserProfileModelTestClass(TestCase):
    """Testing the user profile model"""
    @classmethod
    def setUpTestData(cls):
        """setUpTestData: Run once to set up non-modified data for all class methods."""
        user = User.objects.create(username='test_user', password='test_password')
        profile: Profile = user.profile

        # Populating user profile
        profile.phone_number = '555-555-555'
        profile.street_address = 'test address 1'
        profile.city = 'test city'
        profile.zip_code = '5555'
        profile.save()

    def test_user_label(self):
        profile = User.objects.get(username='test_user').profile
        field_label = profile._meta.get_field('user').verbose_name

        self.assertEqual(field_label, 'user')

    def test_phone_number_label(self):
        profile = User.objects.get(username='test_user').profile
        field_label = profile._meta.get_field('phone_number').verbose_name

        self.assertEqual(field_label, 'phone number')

    def test_phone_number_max_length(self):
        profile = User.objects.get(username='test_user').profile
        expected_length = profile._meta.get_field('phone_number').max_length

        self.assertEqual(expected_length, 12)

    def test_street_address_label(self):
        profile = User.objects.get(username='test_user').profile
        field_label = profile._meta.get_field('street_address').verbose_name

        self.assertEqual(field_label, 'street address')

    def test_street_address_max_length(self):
        profile = User.objects.get(username='test_user').profile
        expected_length = profile._meta.get_field('street_address').max_length

        self.assertEqual(expected_length, 100)

    def test_city_label(self):
        profile = User.objects.get(username='test_user').profile
        field_label = profile._meta.get_field('city').verbose_name

        self.assertEqual(field_label, 'city')

    def test_city_max_length(self):
        profile = User.objects.get(username='test_user').profile
        expected_length = profile._meta.get_field('city').max_length

        self.assertEqual(expected_length, 100)

    def zip_code(self):
        profile = User.objects.get(username='test_user').profile
        field_label = profile._meta.get_field('zip_code').verbose_name

        self.assertEqual(field_label, 'zip code')

    def test_zip_code_max_length(self):
        profile = User.objects.get(username='test_user').profile
        expected_length = profile._meta.get_field('zip_code').max_length

        self.assertEqual(expected_length, 5)

    def test_object_name_is_users_profile(self):
        user = User.objects.get(username='test_user')
        profile = user.profile

        expected_object_name = f"{user.username}'s Profile"
        self.assertEqual(expected_object_name, str(profile))

