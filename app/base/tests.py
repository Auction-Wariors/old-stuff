import datetime

from django.contrib.auth.models import User
from django.test import TestCase, SimpleTestCase
from django.urls import resolve, reverse
from django.test import Client
from django.utils import timezone

from app.auctions.models import Auction, Category
from .views import index
from app.stores.models import Store


class TestUrls(SimpleTestCase):

    def test_index_url_is_resolves(self):
        url = reverse('base:index')
        self.assertEqual(resolve(url).func, index)


class TestView(TestCase):

    def setUp(self):
        # FIXME create objects here, look them up in tests. (dont attach objects to self)
        self.client = Client()
        self.index = reverse('base:index')

        self.user = User.objects.create(username='test', password='test')
        self.store = Store.objects.create(name='test', owner=self.user)
        self.category = Category.objects.create(name='TestCategory', description='TestCategory')

        self.current_datetime = timezone.now()

        Auction.objects.create(name='test_item', description='blabla', category=self.category, store=self.store,
                               start_date=self.current_datetime,
                               end_date=self.current_datetime + datetime.timedelta(days=7))

    def test_index_view_count_auction(self):
        response = self.client.get(self.index)
        Auction.objects.create(name='test_item123', description='blabla', category=self.category, store=self.store,
                               start_date=self.current_datetime,
                               end_date=self.current_datetime + datetime.timedelta(days=7))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Auction.objects.all().count(), 2)
