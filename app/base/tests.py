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

        user = User.objects.create(username='test', password='test')
        store = Store.objects.create(name='test', owner=user)
        category = Category.objects.create(name='TestCategory', description='TestCategory')
        Auction.objects.create(name='test_item', description='blabla', category=category, store=store)

    def test_index_view_count_auction(self):
        response = self.client.get(self.index)

        self.assertEqual(Auction.objects.all().count(), 1)
