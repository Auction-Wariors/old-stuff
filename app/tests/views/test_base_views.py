from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from django.contrib.auth.models import User
from auctions.models import Category, Auction, Bid
from stores.models import Store


class TestBaseViews(TestCase):
    # set up test data for check_auction?

    # def setUpTestData(cls):
    #     category = Category.objects.create(name='Test Category',
    #                                        description='test description')
    #     cls.category2 = Category.objects.create(name='Test Category 2',
    #                                             description='test description')
    #     user = User.objects.create(username='test_user')
    #     cls.user_bid = User.objects.create(username='bid_user', password='bid_user_password')
    #     user.set_password('test123')
    #     user.save()
    #     get_user = User.objects.get(username='test_user')
    #     store = Store.objects.create(name='testStore',
    #                                  owner=get_user,
    #                                  description='test',
    #                                  email='fr@ed.no',
    #                                  phone_number='12345678')
    #
    #     cls.auction = Auction.objects.create(name='test auction',
    #                                          description='test description',
    #                                          category=category,
    #                                          store=store,
    #                                          is_active=True,
    #                                          start_date=timezone.now(),
    #                                          end_date=timezone.now() + timezone.timedelta(days=5),
    #                                          min_price=200,
    #                                          buy_now=300)

    def test_index_get(self):
        response = self.client.get(reverse('base:index'))
        self.assertTemplateUsed(response, 'base/index.html')

    def test_pricing_page(self):
        response = self.client.get(reverse('base:pricing'))
        self.assertTemplateUsed(response, 'base/pricing.html')

    def test_faq_page(self):
        response = self.client.get(reverse('base:faq'))
        self.assertTemplateUsed(response, 'base/faq.html')

    def test_login_page(self):
        response = self.client.get(reverse('base:login'))
        self.assertTemplateUsed(response, 'base/login.html')

