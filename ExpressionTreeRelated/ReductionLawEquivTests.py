import unittest
from InfixToPostfix import InfixToPostfixConverter
from ExpressionTree import ExpressionTree
from ReductionLawEquivTransformer import ReductionLawEquivTransformer

class TestReductionLawEquivTransformer(unittest.TestCase):

    def setUp(self):
        self.law_description = law_description = "Reducing equivalences: (F ↔ G) ~ (F → G) ∧ (G → F)\n"

    def tearDown(self):
        pass

    def test_simple_equiv(self):
        postfix = InfixToPostfixConverter.attempt_conversion("(F↔G)")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.law_description + "((F→G)∧(G→F))", ReductionLawEquivTransformer.apply_law(expression_tree))
    
    def test_nested_equiv(self):
        postfix = InfixToPostfixConverter.attempt_conversion("((F↔G)↔(A↔B))")
        expression_tree = ExpressionTree(postfix)
        expected_str = "((((F→G)∧(G→F))→((A→B)∧(B→A)))∧(((A→B)∧(B→A))→((F→G)∧(G→F))))"
        self.assertEqual(self.law_description + expected_str, ReductionLawEquivTransformer.apply_law(expression_tree))

if __name__ == '__main__':
    unittest.main()