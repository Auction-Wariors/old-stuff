from django.test import TestCase


class TestTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        """setUpTestData: Run once to set up non-modified data for all class methods."""
        pass

    def setUp(self):
        """setUp: Run once for every test method to setup clean data."""
        pass

    def tearDown(self):
        """Clean up run after every test method."""
        pass

    def test_false_is_false(self):
        self.assertFalse(False)

    def test_true_is_true(self):
        self.assertTrue(True)

    def test_one_plus_one_equals_two(self):
        self.assertEqual(1 + 1, 2)
