from unittest import TestCase
from app import app
from flask import session, request
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

class appTest(TestCase):

    def setUp(self):
        """set up before each test"""
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
        

    # def test_users_list():


class UserModelTestCase(TestCase):
    """test User model"""

    def setUp(self):
        """clean up existing users"""

        User.query.delete()

    def tearDown(self):
        """rollback failed transactions"""

        db.session.rollback()

    def test_full_name(self):
        """should create a full name from first and last. Used as property"""

        TestUser = User(first_name="Test-First", last_name="Test-last")
        self.assertEquals(TestUser.make_full_name, "Test-first Test-last")