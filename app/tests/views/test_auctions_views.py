from django.contrib.auth.models import User
from django.test import TestCase
from http import HTTPStatus
from django.utils import timezone
from django.urls import reverse

from auctions.models import Category, Auction, Bid
from stores.models import Store
from auctions.views import count_down_func


class TestAddAuction(TestCase):
    """Testing add auction view"""

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='test',
                                description='test description')
        user = User.objects.create(username='test')
        user.set_password('test123')
        user.save()
        get_user = User.objects.get(username='test')
        Store.objects.create(name='testStore',
                             owner=get_user,
                             description='test',
                             email='fr@ed.no',
                             phone_number='12345678')

    def test_add_auction_view_post_success(self):
        auction_count = Auction.objects.count()

        category = Category.objects.filter(name='test').first()
        end_time = timezone.now() + timezone.timedelta(days=4)

        user_login = self.client.login(username='test', password='test123')
        self.assertTrue(user_login)

        response = self.client.post('/auctions/create/', data={'name': 'item1',
                                                               'description': 'item1 description',
                                                               'category': category.id,
                                                               'end_date': end_time,
                                                               'min_price': 200,
                                                               'buy_now': 1000})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], "/stores/dashboard/")

        auction = Auction.objects.get(name='item1')
        self.assertEqual(Auction.objects.count(), auction_count + 1)
        self.assertEqual(auction.name, 'item1')

    def test_add_auction_view_post_end_date_past_14_days_error(self):
        category = Category.objects.filter(name='test').first()
        end_time = timezone.now() + timezone.timedelta(days=15)

        user_login = self.client.login(username='test', password='test123')
        self.assertTrue(user_login)

        response = self.client.post('/auctions/create/', data={'name': 'item1',
                                                               'description': 'item1 description',
                                                               'category': category.id,
                                                               'end_date': end_time,
                                                               'min_price': 200,
                                                               'buy_now': 1000})
        self.assertFormError(response, 'form', 'end_date', 'End date and time cannot be more than 14 days from now')
        self.assertContains(response, 'End date and time cannot be more than 14 days from now', html=True)
        self.assertEqual(response.status_code, 200)

    def test_add_auction_view_post_end_date_less__than_5_minutes_from_time_auction_added(self):
        category = Category.objects.get(name='test')
        end_time = timezone.now() + timezone.timedelta(minutes=3)

        user_login = self.client.login(username='test', password='test123')
        self.assertTrue(user_login)

        response = self.client.post('/auctions/create/', data={'name': 'item1',
                                                               'description': 'item1 description',
                                                               'category': category.id,
                                                               'end_date': end_time,
                                                               'min_price': 200,
                                                               'buy_now': 100
                                                               })
        self.assertFormError(response, 'form', 'end_date', 'End date and time must be at least 5 minutes from now')
        self.assertContains(response, 'End date and time must be at least 5 minutes from now', html=True)
        self.assertEqual(response.status_code, 200)

    def test_add_auction_view_get(self):
        user_login = self.client.login(username='test', password='test123')
        self.assertTrue(user_login)

        response = self.client.get("/auctions/create/")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, '<legend class="border-bottom mb-4">Create Auction</legend>', html=True)


class TestUpdateAuction(TestCase):
    """Testing update auction view"""

    @classmethod
    def setUpTestData(cls):
        """ Set up test data for update auction"""
        category = Category.objects.create(name='Test Category',
                                           description='test description')
        cls.category2 = Category.objects.create(name='Test Category 2',
                                                description='test description')
        user = User.objects.create(username='test_user')
        cls.user_bid = User.objects.create(username='bid_user', password='bid_user_password')
        user.set_password('test123')
        user.save()
        get_user = User.objects.get(username='test_user')
        store = Store.objects.create(name='testStore',
                                     owner=get_user,
                                     description='test',
                                     email='fr@ed.no',
                                     phone_number='12345678')

        cls.auction = Auction.objects.create(name='test auction',
                                             description='test description',
                                             category=category,
                                             store=store,
                                             is_active=True,
                                             start_date=timezone.now(),
                                             end_date=timezone.now() + timezone.timedelta(days=5),
                                             min_price=200,
                                             buy_now=300)

    def test_update_auction_without_bids(self):
        self.client.login(username='test_user', password='test123')

        response = self.client.post(reverse('auctions:update_auction', kwargs={'auction_id': self.auction.id, }),
                                    data={'name': 'Updated test auction',
                                          'description': 'test description',
                                          'category': self.category2.id,
                                          'min_price': 300
                                          })

        auction_updated = Auction.objects.get(name='Updated test auction')
        self.assertEqual(auction_updated.name, 'Updated test auction')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], "/stores/dashboard/")

    def test_update_auction_with_bids(self):
        self.auction.highest_bid = 300
        self.auction.save()
        self.client.login(username='test_user', password='test123')

        response = self.client.post(reverse('auctions:update_auction', kwargs={'auction_id': self.auction.id, }),
                                    data={'name': 'min_price',
                                          'description': 'test description',
                                          'category': self.category2.id,
                                          })

        auction_updated = Auction.objects.get(name='min_price')
        self.assertEqual(auction_updated.name, 'min_price')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], "/stores/dashboard/")

    def test_update_auction_get(self):
        auction = Auction.objects.get(name='test auction')
        user_login = self.client.login(username='test_user', password='test123')
        self.assertTrue(user_login)

        response = self.client.get(f"/auctions/edit/{auction.id}", follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Update Auction', html=True)
        self.assertTemplateUsed(response, 'auctions/update_auction.html')


class TestBidOnAuction(TestCase):
    """Testing update auction view"""

    @classmethod
    def setUpTestData(cls):
        """ Set up test data for bid on auction"""
        category = Category.objects.create(name='Test Category',
                                           description='test description')
        store_user = User.objects.create(username='store_user')
        store_user.set_password('test123')
        store_user.save()

        user_bid1 = User.objects.create(username='bid_user1')
        user_bid1.set_password('test123')
        user_bid1.save()

        user_bid2 = User.objects.create(username='bid_user2')
        user_bid2.set_password('test123')
        user_bid2.save()

        get_user = User.objects.get(username='store_user')
        store = Store.objects.create(name='testStore',
                                     owner=get_user,
                                     description='test',
                                     email='fr@ed.no',
                                     phone_number='12345678')

        cls.auction = Auction.objects.create(name='test auction',
                                             description='test description',
                                             category=category,
                                             store=store,
                                             is_active=True,
                                             start_date=timezone.now(),
                                             end_date=timezone.now() + timezone.timedelta(days=5),
                                             min_price=30000,
                                             buy_now=10000)

    def test_add_bid_to_auction_success(self):
        user_bid1_login = self.client.login(username='bid_user1', password='test123')
        self.assertTrue(user_bid1_login)

        response = self.client.post(reverse('auctions:auction_detail', kwargs={'pk': self.auction.id, }),
                                    data={'value': 350
                                          })

        bid = Bid.objects.filter(auction=self.auction.id).last()
        self.assertEqual(bid.value, 350*100)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], reverse('auctions:auction_detail', kwargs={'pk': self.auction.id, }))

    def test_add_bid_to_auction_bid_is_lower_than_min_price(self):
        user_bid1_login = self.client.login(username='bid_user1', password='test123')
        self.assertTrue(user_bid1_login)

        response = self.client.post(reverse('auctions:auction_detail', kwargs={'pk': self.auction.id, }),
                                    data={'value': 200
                                          })

        self.assertFormError(response, 'form', 'value', 'Bid is lower than minimum price')
        self.assertContains(response, 'Bid is lower than minimum price', html=True)
        self.assertEqual(response.status_code, 200)

    def test_add_bid_to_auction_bid_to_low(self):
        self.auction.highest_bid = 35000
        self.auction.save()
        user_bid1_login = self.client.login(username='bid_user1', password='test123')
        self.assertTrue(user_bid1_login)

        response = self.client.post(reverse('auctions:auction_detail', kwargs={'pk': self.auction.id, }),
                                    data={'value': 340
                                          })

        self.assertFormError(response, 'form', 'value', 'Bid is too low')
        self.assertContains(response, 'Bid is too low', html=True)
        self.assertEqual(response.status_code, 200)

    def test_add_bid_to_auction_bid_on_own_auction(self):
        self.client.login(username='store_user', password='test123')

        response = self.client.post(reverse('auctions:auction_detail', kwargs={'pk': self.auction.id, }),
                                    data={'value': 500
                                          })

        self.assertFormError(response, 'form', 'value', 'Bidding on your own auction is not allowed')
        self.assertContains(response, 'Bidding on your own auction is not allowed', html=True)
        self.assertEqual(response.status_code, 200)

    def test_add_bid_to_auction_not_active(self):
        self.auction.is_active = False
        self.auction.save()
        user_bid1_login = self.client.login(username='bid_user1', password='test123')
        self.assertTrue(user_bid1_login)

        response = self.client.post(reverse('auctions:auction_detail', kwargs={'pk': self.auction.id, }),
                                    data={'value': 500
                                          })

        self.assertFormError(response, 'form', 'value', 'Auction is not active')
        self.assertContains(response, 'Auction is not active', html=True)
        self.assertEqual(response.status_code, 200)

    def test_add_bid_to_auction_past_end_date(self):
        self.auction.end_date = timezone.now() - timezone.timedelta(days=5)
        self.auction.save()
        user_bid1_login = self.client.login(username='bid_user1', password='test123')
        self.assertTrue(user_bid1_login)

        response = self.client.post(reverse('auctions:auction_detail', kwargs={'pk': self.auction.id, }),
                                    data={'value': 500
                                          })

        self.assertFormError(response, 'form', 'value', 'Auction is ended')
        self.assertEqual(response.status_code, 200)

# FIXME: DOES NOT WORK
# class TestAuctionDetail(TestCase):
#     def test_time_count_down(self):
#         end_time = timezone.now() + timezone.timedelta(hours=5)
#         time = end_time - timezone.now()
#         count_down = count_down_func(time)
#         self.assertEqual(count_down, {'days': 0,
#                                       'hours': 4,
#                                       'minutes': 59,
#                                       'seconds': 59})
