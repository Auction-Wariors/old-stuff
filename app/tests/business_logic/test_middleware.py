from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse

from stores.models import Store
from auctions.models import Category, Auction, Bid

User = get_user_model()


class BidModelTestClass(TestCase):
    """Testing the bid model"""

    @classmethod
    def setUp(cls):
        """setUpTestData: Run once to set up non-modified data for all class methods."""
        user = User.objects.create(username='test', password='test')
        category = Category.objects.create(name='test category')
        store = Store.objects.create(name='test store',
                                     owner=user,
                                     description='test store description',
                                     email='test@teststore.com',
                                     phone_number='555 555 555')
        auction = Auction.objects.create(
            name='test auction',
            description='test auction description',
            category=category,
            store=store,

            # 5 days ago
            start_date=timezone.now() - timezone.timedelta(days=5),
            # 1 hour ago
            end_date=timezone.now() - timezone.timedelta(hours=1),

            min_price=500,
            buy_now=1000
        )
        bid_user = User.objects.create(username='bid user', password='test')
        Bid.objects.create(
            value=5000,
            auction=auction,
            owner=bid_user
        )

    def test_that_middleware_sets_action_is_active_to_false(self):
        response = self.client.get(reverse('base:index'))
        auction = Auction.objects.get(pk=1)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(auction.is_active)

    def test_that_middleware_sets_winning_bid_user_as_auction_winner(self):
        response = self.client.get(reverse('base:index'))
        auction = Auction.objects.get(pk=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(auction.winner, User.objects.get(username='bid user'))


