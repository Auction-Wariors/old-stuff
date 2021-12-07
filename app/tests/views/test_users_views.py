from django.contrib.auth.models import User
from django.contrib import auth
from django.test import TestCase
from http import HTTPStatus
from django.urls import reverse
from django.utils import timezone

from auctions.models import Category, Auction
from stores.models import Store
from users.models import Profile


class TestRegisterUser(TestCase):
    """ Test register user view"""

    def test_registration_user_and_auto_login(self):
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

    def test_register_user_get_request(self):
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

    def test_update_profile_get_request(self):
        self.client.login(username='test_user', password='test')

        response = self.client.get(reverse('users:edit_profile'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit Profile', html=True)
        self.assertTemplateUsed(response, 'users/edit_profile.html')


class TestWonAuction(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='Test Category',
                                           description='test description')
        bid_user = User.objects.create(username='bid_user')
        store_user = User.objects.create(username='store_user', password='store_password')
        bid_user.set_password('test123')
        bid_user.save()
        store = Store.objects.create(name='testStore',
                                     owner=store_user,
                                     description='test',
                                     email='fr@ed.no',
                                     phone_number='12345678')

        auction = Auction.objects.create(name='test auction',
                                         description='test description',
                                         category=category,
                                         store=store,
                                         is_active=True,
                                         start_date=timezone.now(),
                                         end_date=timezone.now() + timezone.timedelta(days=5),
                                         min_price=200,
                                         buy_now=300)

        auction.highest_bid = 350
        auction.winner = bid_user
        auction.is_active = False
        auction.end_date = timezone.now()
        auction.save()

    def test_view_auction_won(self):
        self.client.login(username='bid_user', password='test123')

        response = self.client.get(reverse('users:user_profile'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pay now', html=True)
        self.assertContains(response, '<h4>Won Auctions - Unpaid:</h4>', html=True)
        self.assertTemplateUsed(response, 'users/profile.html')
