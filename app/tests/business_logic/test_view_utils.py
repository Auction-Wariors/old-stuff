from django.test import SimpleTestCase
from django.utils import timezone

from business_logic.view_utils import count_down


class TestAuctionDetail(SimpleTestCase):
    def test_time_count_down(self):
        end_time = timezone.now() + timezone.timedelta(hours=5, seconds=10)
        time = end_time - timezone.now()
        time_left = count_down(time)
        self.assertEqual(time_left, {'days': 0,
                                     'hours': 5,
                                     'minutes': 0})
