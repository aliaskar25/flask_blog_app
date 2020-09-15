import unittest
from app import create_app, db
from app.models import User, Permission, AnonymousUser, Role


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.user = User(password="dog")

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

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

    def test_roles_and_permissions(self):
        u = User(email="some@email.com", password="dog")
        self.assertTrue(u.can(Permission.WRITE_ARTICLES))
        self.assertFalse(u.can(Permission.MODERATE_COMMENTS))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))
