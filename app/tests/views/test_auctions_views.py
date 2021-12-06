from django.contrib.auth.models import User
from django.test import TestCase
from http import HTTPStatus
from django.utils import timezone
from django.urls import reverse

from auctions.models import Category, Auction, Bid
from stores.models import Store


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

    def test_add_auction_view_post_with_buy_now_success(self):
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
        self.assertEqual(auction.buy_now, 100000)

    def test_add_auction_view_post_without_buy_now_success(self):
        auction_count = Auction.objects.count()

        category = Category.objects.filter(name='test').first()
        end_time = timezone.now() + timezone.timedelta(days=4)

        user_login = self.client.login(username='test', password='test123')
        self.assertTrue(user_login)

        response = self.client.post('/auctions/create/', data={'name': 'item1',
                                                               'description': 'item1 description',
                                                               'category': category.id,
                                                               'end_date': end_time,
                                                               'min_price': 200})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], "/stores/dashboard/")

        auction = Auction.objects.get(name='item1')
        self.assertEqual(Auction.objects.count(), auction_count + 1)
        self.assertEqual(auction.name, 'item1')
        self.assertFalse(auction.buy_now)

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

    def test_add_auction_view_post_end_date_less_than_5_minutes_from_time_auction_added_error(self):
        category = Category.objects.get(name='test')
        end_time = timezone.now() + timezone.timedelta(minutes=3)

        user_login = self.client.login(username='test', password='test123')
        self.assertTrue(user_login)

        response = self.client.post('/auctions/create/', data={'name': 'item1',
                                                               'description': 'item1 description',
                                                               'category': category.id,
                                                               'end_date': end_time,
                                                               'min_price': 200,
                                                               'buy_now': 1000
                                                               })
        self.assertFormError(response, 'form', 'end_date', 'End date and time must be at least 5 minutes from now')
        self.assertContains(response, 'End date and time must be at least 5 minutes from now', html=True)
        self.assertEqual(response.status_code, 200)

    def test_add_auction_view_post_buy_now_not_higher_than_min_price(self):
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
        self.assertFormError(response, 'form', 'buy_now', 'Buy now value needs to be higher than minimum price value')
        self.assertContains(response, 'Buy now value needs to be higher than minimum price value', html=True)
        self.assertEqual(response.status_code, 200)

    def test_add_auction_view_get_request(self):
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

    def test_update_auction_get_request(self):
        user_login = self.client.login(username='test_user', password='test123')
        self.assertTrue(user_login)
        self.auction.highest_bid = 1000
        self.auction.save()

        response = self.client.get(f"/auctions/edit/{self.auction.id}", follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Update Auction', html=True)
        self.assertTemplateUsed(response, 'auctions/update_auction.html')

    def test_update_auction_not_active_redirect_to_dashboard(self):
        user_login = self.client.login(username='test_user', password='test123')
        self.assertTrue(user_login)

        self.auction.is_active = False
        self.auction.save()

        response = self.client.get(f"/auctions/edit/{self.auction.id}", follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, reverse('stores:store_dashboard'), status_code=301, target_status_code=200)


class TestBidOnAuction(TestCase):
    """Testing bid on auction view"""

    @classmethod
    def setUpTestData(cls):
        """ Set up test data for bid on auction """
        category = Category.objects.create(name='Test Category',
                                           description='test description')
        store_user = User.objects.create(username='store_user')
        store_user.set_password('test123')
        store_user.save()

        user_bid1 = User.objects.create(username='bid_user1')
        user_bid1.set_password('test123')
        user_bid1.save()

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
                                             buy_now=100000)

    def test_add_bid_to_auction_success(self):
        user_bid1_login = self.client.login(username='bid_user1', password='test123')
        self.assertTrue(user_bid1_login)

        response = self.client.post(reverse('auctions:auction_detail', kwargs={'pk': self.auction.id, }),
                                    data={'value': 350
                                          })

        bid = Bid.objects.filter(auction=self.auction.id).last()
        self.assertEqual(bid.value, 350 * 100)
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


class TestBuyNowAuction(TestCase):
    """Testing buy now auction view"""

    @classmethod
    def setUpTestData(cls):
        """ Set Up Test Data for Auction buy now"""

        category = Category.objects.create(name='Test Category',
                                           description='test description')
        store_user = User.objects.create(username='store_user')
        store_user.set_password('test123')
        store_user.save()

        user_bid1 = User.objects.create(username='bid_user1')
        user_bid1.set_password('test123')
        user_bid1.save()

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
                                             buy_now=100000)

    def test_buy_now_success(self):
        self.client.login(username='bid_user1', password='test123')

        response = self.client.post(reverse('auctions:buy_now_auction', kwargs={'auction_id': self.auction.id, }),
                                    data={'test': 'empty'})

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], reverse('users:user_profile'))

        auction_updated = Auction.objects.get(pk=self.auction.id)
        self.assertEqual(auction_updated.winner.username, 'bid_user1')
        self.assertFalse(auction_updated.is_active)

    def test_buy_now_auction_not_active(self):
        self.auction.is_active = False
        self.auction.save()

        self.client.login(username='bid_user1', password='test123')

        response = self.client.post(reverse('auctions:buy_now_auction', kwargs={'auction_id': self.auction.id, }),
                                    data={'test': 'empty'})

        self.assertContains(response, 'Auction not active...')

    def test_buy_now_user_own_auction(self):
        self.client.login(username='store_user', password='test123')

        response = self.client.get(reverse('auctions:buy_now_auction', kwargs={'auction_id': self.auction.id, }),
                                   follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, reverse('stores:store_dashboard'), status_code=302)

        auction = Auction.objects.get(pk=self.auction.id)
        self.assertFalse(auction.winner)
        self.assertTrue(auction.is_active)

    def test_buy_now_bid_higher_than_or_equal_to_buy_now_price(self):
        self.client.login(username='bid_user1', password='test123')

        self.auction.highest_bid = 100000
        self.auction.save()

        response = self.client.get(reverse('auctions:buy_now_auction',
                                           kwargs={'auction_id': self.auction.id, }), follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, reverse('auctions:auction_detail', kwargs={'pk': self.auction.id, }),
                             status_code=302,
                             target_status_code=200)

        auction = Auction.objects.get(pk=self.auction.id)
        self.assertFalse(auction.winner)
        self.assertTrue(auction.is_active)

    def test_buy_now_get_request(self):
        self.client.login(username='bid_user1', password='test123')

        response = self.client.get(reverse('auctions:buy_now_auction', kwargs={'auction_id': self.auction.id, }),
                                   follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'auctions/buy_now.html')
        self.assertContains(response, '<h3 class="text-muted mb-0">Confirm buy now</h3>', html=True)


class TestPaymentAuction(TestCase):
    """Testing payment auction"""

    @classmethod
    def setUpTestData(cls):
        """ Set Up Test Data for auction payment """

        category = Category.objects.create(name='Test Category',
                                           description='test description')
        store_user = User.objects.create(username='store_user')
        store_user.set_password('test123')
        store_user.save()

        user_bid1 = User.objects.create(username='bid_user1')
        user_bid1.set_password('test123')
        user_bid1.save()

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
                                             buy_now=100000)

    def test_payment_auction_ok(self):
        self.client.login(username='bid_user1', password='test123')
        winner = User.objects.get(username='bid_user1')
        self.auction.winner = winner
        self.auction.highest_bid = 50000
        self.auction.save()

        response = self.client.get(reverse('auctions:payment_ok', kwargs={'auction_id': self.auction.id, }),
                                   follow=True)

        self.assertRedirects(response, reverse('users:user_profile'),
                             status_code=302,
                             target_status_code=200)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Payment successful! Total amount payed: NOK 500.0,- ')

    def test_payment_auction_fail(self):
        self.client.login(username='bid_user1', password='test123')
        winner = User.objects.get(username='bid_user1')
        self.auction.winner = winner
        self.auction.highest_bid = 50000
        self.auction.save()

        response = self.client.post(reverse('auctions:payment_auction',
                                            kwargs={'auction_id': self.auction.id, }),
                                    data={'test': 'empty'})

        self.assertEqual(response["Location"],
                         reverse('auctions:payment_auction', kwargs={'auction_id': self.auction.id}))

    def test_payment_is_paid(self):
        self.client.login(username='bid_user1', password='test123')
        winner = User.objects.get(username='bid_user1')
        self.auction.is_payed = True
        self.auction.winner = winner
        self.auction.highest_bid = 50000
        self.auction.save()

        response = self.client.get(reverse('auctions:payment_auction',
                                           kwargs={'auction_id': self.auction.id, }), follow=True)

        self.assertRedirects(response, reverse('users:user_profile'),
                             status_code=302,
                             target_status_code=200)

    def test_payment_get_request(self):
        self.client.login(username='bid_user1', password='test123')
        winner = User.objects.get(username='bid_user1')
        self.auction.winner = winner
        self.auction.highest_bid = 50000
        self.auction.save()

        response = self.client.get(reverse('auctions:payment_auction',
                                           kwargs={'auction_id': self.auction.id, }))

        self.assertTemplateUsed(response, 'auctions/payment.html')
        self.assertContains(response, 'Pay OK', html=True)
        self.assertContains(response, 'Pay FAIL', html=True)
