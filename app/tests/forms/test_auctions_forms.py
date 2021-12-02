from django.test import TestCase
from django.utils import timezone

from auctions.forms import AddAuctionForm
from auctions.models import Category


class TestAuctionForms(TestCase):

    def setUp(self):
        Category.objects.create(name='test',
                                description='test description')

    def test_add_auction_form_is_valid(self):
        category = Category.objects.filter(name='test').first()
        end_time = timezone.now() + timezone.timedelta(days=4)
        i_form = AddAuctionForm(data={
            'name': 'item1',
            'description': 'item1 description',
            'category': category,
            'end_date': end_time,
            'min_price': 200,
        })

        self.assertTrue(i_form.is_valid())

    def test_add_auction_form_end_time_past_14_days_error(self):
        category = Category.objects.get(name='test')
        end_time = timezone.now() + timezone.timedelta(days=15)
        i_form = AddAuctionForm(data={
            'name': 'item1',
            'description': 'item1 description',
            'category': category,
            'end_date': end_time,
            'min_price': 200,
        })

        self.assertEqual(len(i_form.errors), 1)

    def test_add_auction_form_end_time_min_5_min_error(self):
        category = Category.objects.get(name='test')
        end_time = timezone.now() + timezone.timedelta(minutes=3)
        i_form = AddAuctionForm(data={
            'name': 'item1',
            'description': 'item1 description',
            'category': category,
            'end_date': end_time,
            'min_price': 200,
        })

        self.assertEqual(len(i_form.errors), 1)

    def test_add_auction_form_no_data(self):
        a_form = AddAuctionForm(data={})

        self.assertFalse(a_form.is_valid())
        self.assertEqual(len(a_form.errors), 5)


