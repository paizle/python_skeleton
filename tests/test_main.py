# tests/test_main.py
import unittest
from app.main import main

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

if __name__ == '__main__':
    unittest.main()
