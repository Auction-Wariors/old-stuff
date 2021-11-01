from django.test import TestCase

from auctions.forms import AddItemForm, AddAuctionForm
from auctions.models import Category


class TestForms(TestCase):

    def setUp(self):
        self.test = Category.objects.create(name='test',
                                       description='test descirpton')

    def test_add_item_form_is_valid(self):

        i_form = AddItemForm(data={
            'name': 'item1',
            'description': 'item1 description',
            'category': self.test
        })

        self.assertTrue(i_form.is_valid())

    def test_add_item_form_no_data(self):
        i_form = AddItemForm(data={})

        self.assertFalse(i_form.is_valid())
        self.assertEqual(len(i_form.errors), 3)

    def test_add_auction_form_is_valid(self):
        a_form = AddAuctionForm(data={
            'start_date': '2022-01-01',
            'end_date': '2022-01-01',
            'min_price': 200
        })

        self.assertTrue(a_form.is_valid())

    def test_add_auction_form_no_data(self):
        a_form = AddAuctionForm(data={})

        self.assertFalse(a_form.is_valid())
        self.assertEqual(len(a_form.errors), 3)




