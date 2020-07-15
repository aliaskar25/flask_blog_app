import unittest
from app.models import User


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.user = User(password="dog")

    def test_password_setter(self):
        self.assertTrue(self.user.password_hash is not None)

    def test_no_password_getter(self):
        with self.assertRaises(AttributeError):
            self.user.password

    def test_password_verification(self):
        self.assertTrue(self.user.verify_password("dog"))
        self.assertFalse(self.user.verify_password("cat"))

    def test_password_salts_are_random(self):
        user2 = User(password="cat")
        self.assertTrue(
            self.user.password_hash != user2.password_hash
        )
