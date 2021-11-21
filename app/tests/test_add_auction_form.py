from django.contrib.auth.models import User
from django.test import TestCase
from http import HTTPStatus

from auctions.forms import AddAuctionForm
from auctions.models import Category, Auction
from stores.models import Store


class TestAuctionForms(TestCase):

    def setUp(self):
        user = User.objects.create(username='test', password='test123')
        Store.objects.create(owner=user)
        Category.objects.create(name='test',
                                description='test description')

    def test_add_auction_form_is_valid(self):
        category = Category.objects.filter(name='test').first()
        i_form = AddAuctionForm(data={
            'name': 'item1',
            'description': 'item1 description',
            'category': category,
            'end_date': '2021-12-02',
            'min_price': 200,
        })
        self.assertTrue(i_form.is_valid())

    def test_add_auction_form_no_data(self):
        a_form = AddAuctionForm(data={})

        self.assertFalse(a_form.is_valid())
        self.assertEqual(len(a_form.errors), 5)


class TestAuctionViews(TestCase):
    def setUp(self):
        Category.objects.create(name='test',
                                description='test description')
        user = User.objects.create(username='test')
        user.set_password('test123')
        user.save()
        get_user = User.objects.get(username='test')
        self.store = Store.objects.create(name='testStore',
                                          owner=get_user,
                                          description='test',
                                          email='fr@ed.no',
                                          phone_number='12345678')

    def test_add_auction_view_post(self):
        auction_count = Auction.objects.count()

        category = Category.objects.filter(name='test').first()

        user_login = self.client.login(username='test', password='test123')
        self.assertTrue(user_login)

        response = self.client.post('/auctions/create/', data={'name': 'item1',
                                                               'description': 'item1 description',
                                                               'category': category.id,
                                                               'end_date': '2021-12-02',
                                                               'min_price': 200})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], "/stores/dashboard/")

        self.assertEqual(Auction.objects.count(), auction_count + 1)

    def test_add_auction_view_get(self):
        user_login = self.client.login(username='test', password='test123')
        self.assertTrue(user_login)

        response = self.client.get("/auctions/create/")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, '<legend class="border-bottom mb-4">Create Auction</legend>', html=True)
