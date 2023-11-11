import unittest
from Clause import Clause
from ClauseSet import ClauseSet
from DP import DavisPutnamTransformer

class TestResolution(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_not_satisfiable(self):
        clause_set = ClauseSet()
        clause_set.add_clause({1, -2})      # 1
        clause_set.add_clause({1, 3})       # 2
        clause_set.add_clause({-2, 3})      # 3
        clause_set.add_clause({-1, 2})      # 4
        clause_set.add_clause({2, -3})      # 5
        clause_set.add_clause({-1, -3})     # 6

        self.assertEqual(False, DavisPutnamTransformer.apply_DP(clause_set))

    def test_satisfiable(self):
        clause_set = ClauseSet()
        clause_set.add_clause({1, -2})      # 1
        clause_set.add_clause({2, 3})       # 2
        clause_set.add_clause({4, 5})       # 3

        self.assertEqual(True, DavisPutnamTransformer.apply_DP(clause_set))

if __name__ == '__main__':
    unittest.main()