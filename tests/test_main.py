# tests/test_main.py
import unittest
from app.main import main, is_prime

class TestMain(unittest.TestCase):
    def test_main_runs(self):
        # Redirect output for testing
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__

        self.assertIn("Hello from app!", captured_output.getvalue())

    def test_is_prime(self):
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(3))
        self.assertTrue(is_prime(5))
        self.assertTrue(is_prime(7))
        self.assertTrue(is_prime(11))
        self.assertFalse(is_prime(1))
        self.assertFalse(is_prime(4))
        self.assertFalse(is_prime(6))
        self.assertFalse(is_prime(8))
        self.assertFalse(is_prime(9))
        self.assertFalse(is_prime(10))
        self.assertFalse(is_prime(0))
        self.assertFalse(is_prime(-1))

if __name__ == '__main__':
    unittest.main()
