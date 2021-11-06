from django.contrib.auth.models import User
from django.test import TestCase

from app.auctions.forms import AddAuctionForm
from app.auctions.models import Category, Auction
from app.stores.models import Store


class TestAuctionForms(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test', password='test123')
        self.store = Store.objects.create(owner=self.user)
        self.category = Category.objects.create(name='test',
                                                description='test description')

    def test_add_auction_form_is_valid(self):
        i_form = AddAuctionForm(data={
            'name': 'item1',
            'description': 'item1 description',
            'category': self.category,
            'start_date': '2022-01-01',
            'end_date': '2022-01-01',
            'min_price': 200,
        })

        self.assertTrue(i_form.is_valid())

    def test_add_auction_form_no_data(self):
        a_form = AddAuctionForm(data={})

        self.assertFalse(a_form.is_valid())
        self.assertEqual(len(a_form.errors), 6)


class TestAuctionViews(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='test',
                                                description='test description')
        self.user = User.objects.create(username='test', password='test123')

    def test_add_action_view(self):
        a_form = {'a_form': 'True',
                  'start_date': '2022-01-01',
                  'end_date': '2022-01-02',
                  'min_price': 250,
                  'name': 'test_product',
                  'description': 'test test',
                  'category': self.category}

        response = self.client.post('/auctions/create/',
                                    a_form)
        self.assertEqual(response.status_code, 200)

