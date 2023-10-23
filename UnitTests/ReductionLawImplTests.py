import unittest
from InfixToPostfix import InfixToPostfixConverter
from ExpressionTree import ExpressionTree
from ReductionLawImplTransformer import ReductionLawImplTransformer

class TestReductionLawImplTransformer(unittest.TestCase):

    def setUp(self):
        self.law_description = law_description = "Reducing implications: (F → G) ~ (¬F ∨ G)\n"

    def tearDown(self):
        pass

    def test_simple_impl(self):
        postfix = InfixToPostfixConverter.attempt_conversion("(F→G)")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.law_description + "((¬F)∨G)", ReductionLawImplTransformer.apply_law(expression_tree))
    
    def test_nested_impl(self):
        postfix = InfixToPostfixConverter.attempt_conversion("((F→G)→(A→B))")
        expression_tree = ExpressionTree(postfix)
        expected_str = "((¬((¬F)∨G))∨((¬A)∨B))"
        self.assertEqual(self.law_description + expected_str, ReductionLawImplTransformer.apply_law(expression_tree))

if __name__ == '__main__':
    unittest.main()