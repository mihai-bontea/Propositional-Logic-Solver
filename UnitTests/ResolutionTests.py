import unittest
from ClauseSet import ClauseSet
from ResolutionTransformer import ResolutionTransformer

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

        resolution_result = ResolutionTransformer.apply_resolution(clause_set)
        self.assertEqual(False, resolution_result.result)

if __name__ == '__main__':
    unittest.main()