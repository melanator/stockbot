import unittest
import query
import yahoo


class QueryTest(unittest.TestCase):
    def test_find_ticker(self):
        self.assertEqual(yahoo.find_ticker('SBER', 'ME'), True)
        self.assertEqual(yahoo.find_ticker('AAPL', 'ME'), False)
        self.assertEqual(yahoo.find_ticker('AAPL', 'NSDQ'), True)

if __name__ == '__main__':
    unittest.main()