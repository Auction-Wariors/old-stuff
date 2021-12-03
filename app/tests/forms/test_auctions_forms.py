from django.test import TestCase
from django.utils import timezone

from django.contrib.auth.models import User
from auctions.forms import AddAuctionForm, UpdateAuctionForm
from auctions.models import Category, Auction
from stores.models import Store


class TestAddAuctionForms(TestCase):

    def setUp(self):
        """ Set up test data for add auction form"""
        Category.objects.create(name='test',
                                description='test description')

    def test_add_auction_form_is_valid(self):
        category = Category.objects.filter(name='test').first()
        end_time = timezone.now() + timezone.timedelta(days=4)
        form = AddAuctionForm(data={
            'name': 'item1',
            'description': 'item1 description',
            'category': category,
            'end_date': end_time,
            'min_price': 200,
        })

        self.assertTrue(form.is_valid())

    def test_add_auction_form_end_time_past_14_days_error(self):
        category = Category.objects.get(name='test')
        end_time = timezone.now() + timezone.timedelta(days=15)
        form = AddAuctionForm(data={
            'name': 'item1',
            'description': 'item1 description',
            'category': category,
            'end_date': end_time,
            'min_price': 200,
        })

        self.assertEqual(len(form.errors), 1)

    def test_add_auction_form_end_time_min_5_min_error(self):
        category = Category.objects.get(name='test')
        end_time = timezone.now() + timezone.timedelta(minutes=3)
        form = AddAuctionForm(data={
            'name': 'item1',
            'description': 'item1 description',
            'category': category,
            'end_date': end_time,
            'min_price': 200,
        })

        self.assertEqual(len(form.errors), 1)

    def test_add_auction_form_no_data(self):
        a_form = AddAuctionForm(data={})

        self.assertFalse(a_form.is_valid())
        self.assertEqual(len(a_form.errors), 5)


class TestUpdateAuctionForms(TestCase):

    def setUp(self):
        """ Set up test data for update auction form"""
        self.category = Category.objects.create(name='test',
                                                description='test description')
        user = User.objects.create(username='test_user', password='test')
        store = Store.objects.create(name='testStore1',
                                     owner=user,
                                     description='test',
                                     email='fr@ed.no',
                                     phone_number='12345678')
        self.auction = Auction.objects.create(name='test auction',
                                              description='test description',
                                              category=self.category,
                                              store=store,
                                              is_active=True,
                                              start_date=timezone.now(),
                                              end_date=timezone.now() + timezone.timedelta(days=5),
                                              min_price=2000,
                                              buy_now=3000)

    def test_update_auction_form_no_bids_is_valid(self):
        form = UpdateAuctionForm(instance=self.auction, bid=False, data={'name': 'item1',
                                                                         'description': 'item1 description',
                                                                         'category': self.category,
                                                                         'min_price': 20})
        self.assertTrue(form.is_valid())

    def test_update_auction_form_no_bids_is_not_valid(self):
        form = UpdateAuctionForm(instance=self.auction, bid=False, data={'name': 'item1',
                                                                         'description': 'item1 description',
                                                                         'category': self.category})
        self.assertFalse(form.is_valid())

    def test_update_auction_form_with_bids_is_valid(self):
        form = UpdateAuctionForm(instance=self.auction, bid=True, data={'name': 'item1',
                                                                        'description': 'item1 description',
                                                                        'category': self.category})
        self.assertTrue(form.is_valid())
