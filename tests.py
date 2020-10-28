import unittest
import query


class QueryTest(unittest.TestCase):
    def test_fetch(self):
        true_query = 'SELECT * from holders WHERE id = 227627486 and name = "melanator"'
        self.assertEqual(query.fetch('holders', id=227627486, name='melanator'), true_query)
    
    def test_update(self):
        true_query = 'UPDATE portfolios SET name = "Govno" WHERE id = 1'
        self.assertEqual(query.update('portfolios', 1, name='"Govno"'), true_query)      


if __name__ == '__main__':
    unittest.main()