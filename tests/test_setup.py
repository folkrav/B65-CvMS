import unittest
from flask import current_app
from app import create_app, db


class SetupTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.context = self.app.app_context()
        self.context.push()
        #db.create_all()

    def teardown(self):
        #db.session_remove()
        #db.drop_all()
        self.context.pop()

    def test_testsworking(self):
        self.assertTrue(True)

    def test_app_is_in_testing(self):
        self.assertTrue(current_app.config['TESTING'])
