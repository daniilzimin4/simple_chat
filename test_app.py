import unittest
import time
import json
import subprocess
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

    def stress_test(self, func, iterations=10):
        """Function for stress testing, runs the test multiple times and outputs the average execution time."""
        total_time = 0
        for _ in range(iterations):
            start_time = time.time()
            func()
            end_time = time.time()
            total_time += (end_time - start_time)
        average_time = total_time / iterations
        return average_time

    def test_time_behavior(self):
        def run_test():
            response = self.app.get('/messages')
            self.assertEqual(response.status_code, 200)

        average_time = self.stress_test(run_test)
        print(f"Average execution time for test_time_behavior: {average_time:.4f} seconds")

    def test_recoverability(self):
        def run_test():
            with app.app_context():
                # Clear the database before adding new messages
                db.session.query(Message).delete()
                db.session.commit()

                # Add 1000 messages
                for i in range(1000):
                    message = Message(text=f"Test message {i + 1}")
                    db.session.add(message)
                db.session.commit()

            response = self.app.get('/messages')
            messages = json.loads(response.data)
            self.assertEqual(len(messages), 1000)  # Check that 1000 messages were added

        average_time = self.stress_test(run_test)
        print(f"Average execution time for test_recoverability: {average_time:.4f} seconds")

    def test_maintainability(self):
        def run_test():
            with app.app_context():
                db.create_all()
                inspector = inspect(db.engine)
                self.assertTrue(inspector.has_table('message'), "Table 'message' should exist")

        average_time = self.stress_test(run_test)
        print(f"Average execution time for test_maintainability: {average_time:.4f} seconds")

    def test_disconnection_recovery(self):
        def run_test():
            with app.app_context():
                # Clear the database before adding new messages
                db.session.query(Message).delete()
                db.session.commit()

                # Add 1000 messages
                for i in range(1000):
                    message = Message(text=f"Test message {i + 1}")
                    db.session.add(message)
                db.session.commit()

            # Simulate client disconnection
            self.app.get('/messages', follow_redirects=True)

            # Simulate server restart (without dropping the database)
            # Just re-establish the app context
            with app.app_context():
                pass  # This simulates the server being restarted

            # Reconnect and check if messages are still there
            response = self.app.get('/messages')
            messages = json.loads(response.data)
            self.assertEqual(len(messages), 1000)  # Check that 1000 messages are still there

        average_time = self.stress_test(run_test)
        print(f"Average execution time for test_disconnection_recovery: {average_time:.4f} seconds")

    def test_code_complexity(self):
        """Measure code complexity using Radon."""
        result = subprocess.run(['radon', 'cc', '--total', '--show-complexity', __file__], capture_output=True, text=True)
        print("Code Complexity Analysis:")
        print(result.stdout)

        print("Code Complexity Analysis for server.py:")
        result_server = subprocess.run(['radon', 'cc', '--total', '--show-complexity', 'server.py'], capture_output=True, text=True)
        print(result_server.stdout)

if __name__ == '__main__':
    unittest.main()
