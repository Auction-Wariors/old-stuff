from auctions.views import count_down_func
from django.test import SimpleTestCase
from django.utils import timezone


class TestAuctionDetail(SimpleTestCase):
    def test_time_count_down(self):
        end_time = timezone.now() + timezone.timedelta(hours=5, seconds=10)
        time = end_time - timezone.now()
        count_down = count_down_func(time)
        self.assertEqual(count_down, {'days': 0,
                                      'hours': 5,
                                      'minutes': 0})
