from django.test import SimpleTestCase

from base.templatetags.currency_tags import divide_by_100, global_raise_value


class TestDivideBy100(SimpleTestCase):
    def test_1000_divided_by_100_equals_10(self):
        self.assertEqual(divide_by_100(1000), 10)

    def test_10000_divided_by_100_not_equals_1(self):
        self.assertNotEqual(divide_by_100(10000), 1)

    def test_none_value_error(self):
        self.failUnlessRaises(ValueError, divide_by_100, '')


class TestGlobalRaiseValue(SimpleTestCase):
    def test_100_returns_105(self):
        self.assertEqual(global_raise_value(100), 105)

    def test_103_not_returns_106(self):
        self.assertNotEqual(global_raise_value(103), 106)

    def test_none_value_error(self):
        self.failUnlessRaises(ValueError, global_raise_value, '')
