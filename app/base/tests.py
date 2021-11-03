from django.contrib.auth.models import User
from django.test import TestCase, SimpleTestCase
from django.urls import resolve, reverse
from django.test import Client

from auctions.models import Auction, Category
from .views import index
from stores.models import Store


class TestUrls(SimpleTestCase):

    def test_index_url_is_resolves(self):
        url = reverse('base:index')
        self.assertEqual(resolve(url).func, index)


class TestView(TestCase):

    def setUp(self):
        self.client = Client()
        self.index = reverse('base:index')

        self.user = User.objects.create(username='test', password='test')
        self.store = Store.objects.create(name='test', owner=self.user)
        self.category = Category.objects.create(name='TestCategory', description='TestCategory')
        Auction.objects.create(name='test_item', description='blabla', category=self.category, store=self.store)

    def test_index_view_count_auction(self):
        response = self.client.get(self.index)
        Auction.objects.create(name='test_item123', description='blabla', category=self.category, store=self.store)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Auction.objects.all().count(), 2)
