from django.contrib.auth.models import User
from django.contrib import auth
from django.test import TestCase
from http import HTTPStatus
from django.urls import reverse
from django.utils import timezone
from users.models import Profile


class TestRegisterUser(TestCase):
    """ Test register user view"""

    def test_register_user(self):
        response = self.client.post(reverse('users:register'), data={'username': 'test_user',
                                                                     'first_name': 'first',
                                                                     'last_name': 'last',
                                                                     'email': 'test@user.com',
                                                                     'password1': 'test_password',
                                                                     'password2': 'test_password'})
        user = auth.get_user(self.client)
        assert user.is_authenticated
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], reverse('base:index'))

        # Profile created
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.user, user)

    def test_register_get(self):
        response = self.client.get(reverse('users:register'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign Up', html=True)
        self.assertTemplateUsed(response, 'users/register.html')


class TestUpdateProfile(TestCase):
    @classmethod
    def setUpTestData(cls):
        """ Set Up Test Data for Update Profile """
        user = User.objects.create(username='test_user')
        user.set_password('test')
        user.save()

    def test_update_profile_success(self):
        self.client.login(username='test_user', password='test')

        response = self.client.post(reverse('users:edit_profile'), data={'first_name': 'first',
                                                                         'last_name': 'last',
                                                                         'email': 'test@user.com',
                                                                         'phone_number': '12345678',
                                                                         'street_address': 'street 1',
                                                                         'city': 'Oslo',
                                                                         'zip_code': '0451'})

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], reverse('users:user_profile'))

        user_updated = auth.get_user(self.client)
        profile = Profile.objects.get(user=user_updated)
        self.assertEqual(user_updated.first_name, 'first')
        self.assertEqual(profile.city, 'Oslo')

    def test_update_profile_get(self):
        self.client.login(username='test_user', password='test')

        response = self.client.get(reverse('users:edit_profile'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit Profile', html=True)
        self.assertTemplateUsed(response, 'users/edit_profile.html')
