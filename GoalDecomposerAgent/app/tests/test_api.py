import unittest

from app.main import home


class ApiSmokeTests(unittest.TestCase):
    def test_home(self):
        response = home()
        self.assertEqual(response["message"], "Goal Decomposer Agent API is running!")


if __name__ == "__main__":
    unittest.main()
