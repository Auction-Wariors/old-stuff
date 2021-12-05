from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from users.models import Profile
from stores.models import Store
from auctions.models import Auction, Category, Bid

User = get_user_model()


class AuctionModelInitialTestClass(TestCase):
    """"Initial tests"""

    @classmethod
    def setUpTestData(cls):
        """setUpTestData: Run once to set up non-modified data for all class methods."""
        user = User.objects.create(username='test', password='test')
        cls.category = Category.objects.create(name='test category')
        cls.store = Store.objects.create(name='test store',
                                         owner=user,
                                         description='test store description',
                                         email='test@teststore.com',
                                         phone_number='555 555 555')

    def test_create_and_retrieve_auction(self):
        auction = Auction.objects.create(
            name='test auction',
            description='test auction description',
            category=self.category,
            store=self.store,
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=5),
            min_price=500,
            buy_now=1000
        )

        self.assertEqual(Auction.objects.get(pk=1), auction)


class BidModelInitialTestClass(TestCase):
    """"Initial tests"""

    @classmethod
    def setUpTestData(cls):
        """setUpTestData: Run once to set up non-modified data for all class methods."""
        user = User.objects.create(username='test', password='test')
        category = Category.objects.create(name='test category')
        store = Store.objects.create(name='test store',
                                     owner=user,
                                     description='test store description',
                                     email='test@teststore.com',
                                     phone_number='555 555 555')
        cls.bid_user = User.objects.create(username='bid user', password='test')
        cls.category = category
        cls.store = store

        cls.auction = Auction.objects.create(
            name='test auction',
            description='test auction description',
            category=category,
            store=store,
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=5),
            min_price=500,
            buy_now=1000
        )

    def test_create_and_retrieve_bid(self):
        bid = Bid.objects.create(
            value=5000,
            auction=self.auction,
            owner=self.bid_user
        )

        self.assertEqual(Bid.objects.get(pk=1), bid)


class AuctionModelTestClass(TestCase):
    """Testing the auction model"""

    @classmethod
    def setUpTestData(cls):
        """setUpTestData: Run once to set up non-modified data for all class methods."""
        user = User.objects.create(username='test', password='test')
        category = Category.objects.create(name='test category')
        store = Store.objects.create(name='test store',
                                     owner=user,
                                     description='test store description',
                                     email='test@teststore.com',
                                     phone_number='555 555 555')
        cls.category = category
        cls.store = store
        cls.auction = Auction.objects.create(
            name='test auction',
            description='test auction description',
            category=category,
            store=store,
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=5),
            min_price=500,
            buy_now=1000
        )

    def test_auction_fields_label(self):
        self.assertEqual(self.auction._meta.get_field('name').verbose_name, 'name')
        self.assertEqual(self.auction._meta.get_field('description').verbose_name, 'description')
        self.assertEqual(self.auction._meta.get_field('category').verbose_name, 'category')
        self.assertEqual(self.auction._meta.get_field('store').verbose_name, 'store')
        self.assertEqual(self.auction._meta.get_field('is_active').verbose_name, 'is active')
        self.assertEqual(self.auction._meta.get_field('start_date').verbose_name, 'start date')
        self.assertEqual(self.auction._meta.get_field('end_date').verbose_name, 'end date')
        self.assertEqual(self.auction._meta.get_field('highest_bid').verbose_name, 'highest bid')
        self.assertEqual(self.auction._meta.get_field('winner').verbose_name, 'winner')
        self.assertEqual(self.auction._meta.get_field('is_payed').verbose_name, 'is payed')
        self.assertEqual(self.auction._meta.get_field('commission_is_payed').verbose_name, 'commission is payed')
        self.assertEqual(self.auction._meta.get_field('min_price').verbose_name, 'min price')
        self.assertEqual(self.auction._meta.get_field('buy_now').verbose_name, 'buy now')

    def test_auction_fields_max_length(self):
        self.assertEqual(self.auction._meta.get_field('name').max_length, 50)
        self.assertEqual(self.auction._meta.get_field('description').max_length, 5000)

    def test_auction_fields_default_value(self):
        self.assertEqual(self.auction._meta.get_field('is_active').default, True)
        self.assertEqual(self.auction._meta.get_field('is_payed').default, False)
        self.assertEqual(self.auction._meta.get_field('commission_is_payed').default, False)

    def test_auction_model__str__(self):
        expected_object_name = "Auction: " + self.auction.name
        self.assertEqual(expected_object_name, str(self.auction))


class BidModelTestClass(TestCase):
    """Testing the bid model"""

    @classmethod
    def setUpTestData(cls):
        """setUpTestData: Run once to set up non-modified data for all class methods."""
        user = User.objects.create(username='test', password='test')
        category = Category.objects.create(name='test category')
        store = Store.objects.create(name='test store',
                                     owner=user,
                                     description='test store description',
                                     email='test@teststore.com',
                                     phone_number='555 555 555')
        category = category
        store = store
        auction = Auction.objects.create(
            name='test auction',
            description='test auction description',
            category=category,
            store=store,
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=5),
            min_price=500,
            buy_now=1000
        )
        bid_user = User.objects.create(username='bid user', password='test')
        cls.bid = Bid.objects.create(
            value=5000,
            auction=auction,
            owner=bid_user
        )

    def test_bid_fields_label(self):
        self.assertEqual(self.bid._meta.get_field('created_at').verbose_name, 'created at')
        self.assertEqual(self.bid._meta.get_field('updated_at').verbose_name, 'updated at')
        self.assertEqual(self.bid._meta.get_field('value').verbose_name, 'value')
        self.assertEqual(self.bid._meta.get_field('auction').verbose_name, 'auction')
        self.assertEqual(self.bid._meta.get_field('owner').verbose_name, 'owner')

    def test_bid_model__str__(self):
        expected_object_name = f"Auction: {self.bid.auction.name} Bid: {self.bid.value}"
        self.assertEqual(expected_object_name, str(self.bid))
