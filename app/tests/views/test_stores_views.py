from django.contrib.auth.models import User
from django.test import TestCase
from http import HTTPStatus
from django.urls import reverse
from django.utils import timezone

from auctions.models import Category, Auction
from stores.models import Store


class TestCreateStore(TestCase):
    """Testing Create Store"""

    @classmethod
    def setUpTestData(cls):
        """ Set up test data for create store"""
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


class TestUpdateStoreProfile(TestCase):
    """Testing Update Store Profile"""

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='test_user')
        user.set_password('test123')
        user.save()
        get_user = User.objects.get(username='test_user')
        Store.objects.create(name='testStore',
                             owner=get_user,
                             description='test',
                             email='test@teststore.com',
                             phone_number='12345678')

    def test_update_store_success(self):
        self.client.login(username='test_user', password='test123')

        response = self.client.post(reverse('stores:update_store'), data={'name': 'Test store updated',
                                                                          'description': 'test updated',
                                                                          'email': 'new@email.com',
                                                                          'phone_number': '87654321'})
        store_updated = Store.objects.get(name='Test store updated')
        self.assertEqual(store_updated.name, 'Test store updated')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], reverse('stores:store_dashboard'))

    def test_update_store_get(self):
        self.client.login(username='test_user', password='test123')

        response = self.client.get(reverse('stores:update_store'), follow=True)
        self.assertTemplateUsed(response, 'stores/update_store.html')
        self.assertContains(response, 'Update your store information', html=True)


class TestStoreDashboard(TestCase):
    """Testing bid on auction view"""

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='Test Category',
                                           description='test description')
        store_user = User.objects.create(username='store_user')
        store_user.set_password('test123')
        store_user.save()

        user_bid1 = User.objects.create(username='bid_user1', password='bid_user1')

        get_user = User.objects.get(username='store_user')
        store = Store.objects.create(name='testStore',
                                     owner=get_user,
                                     description='test',
                                     email='fr@ed.no',
                                     phone_number='12345678')

        cls.auction = Auction.objects.create(name='test auction',
                                             description='test description',
                                             category=category,
                                             store=store,
                                             is_active=True,
                                             start_date=timezone.now(),
                                             end_date=timezone.now() + timezone.timedelta(days=5),
                                             min_price=30000,
                                             buy_now=100000,
                                             highest_bid=100000,
                                             commission_is_payed=False,
                                             winner=user_bid1)

    def test_store_dashboard(self):
        self.client.login(username='store_user', password='test123')

        response = self.client.get(reverse('stores:store_dashboard'))

        self.assertTemplateUsed(response, 'stores/dashboard.html')
        self.assertContains(response, 'testStore', html=True)

    def test_store_dashboard_pay_commission_success(self):
        self.client.login(username='store_user', password='test123')

        response = self.client.get(reverse('stores:store_dashboard'), {'payment': 'ok', 'auction': self.auction.id})

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Thank you for your business! ')

    def test_store_dashboard_pay_commission_fail(self):
        self.client.login(username='store_user', password='test123')

        response = self.client.get(reverse('stores:store_dashboard'), {'payment': 'failed'})

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Payment failed, please contact your bank! ')
