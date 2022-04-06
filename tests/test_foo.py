import unittest

class TestFoo(unittest.TestCase):

    def test_lower(self):
        msg = 'Foo'
        self.assertEqual(msg.lower(), 'foo')

