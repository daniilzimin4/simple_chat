import unittest
import time
import json
from server import app, db, Message
from sqlalchemy import inspect


class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            db.create_all()
            db.session.begin_nested()

    def tearDown(self):
        with app.app_context():
            db.session.rollback()
            db.drop_all()

    def test_time_behavior(self):
        start_time = time.time()
        response = self.app.get('/messages')
        end_time = time.time()
        self.assertEqual(response.status_code, 200)
        self.assertLess(end_time - start_time, 1, "Response time is too slow!")

    def test_recoverability(self):
        with app.app_context():
            message = Message(text="Test message")
            db.session.add(message)
            db.session.commit()

        response = self.app.get('/messages')
        messages = json.loads(response.data)
        self.assertIn("Test message", [msg['text'] for msg in messages])

    def test_maintainability(self):
        with app.app_context():
            db.create_all()
            inspector = inspect(db.engine)
            self.assertTrue(inspector.has_table('message'), "Table 'message' should exist")


if __name__ == '__main__':
    unittest.main()
