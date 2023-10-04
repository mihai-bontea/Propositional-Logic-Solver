import unittest
from InfixToPostfix import InfixToPostfixConverter
from ExpressionTree import ExpressionTree
from NegationLawTransformer import NegationLawTransformer

class TestNegationLawTransformer(unittest.TestCase):

    def setUp(self):
        self.law_description = "Applying negation laws: ¬(¬F) ~ F, ¬(F → G) ~ F ∧ (¬G), ¬(F ↔ G) ~ F ↔ (¬G)\n"

    def tearDown(self):
        pass

    def test_even_negation(self):
        postfix = InfixToPostfixConverter.attempt_conversion("(¬(¬(¬(¬A))))")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.law_description + "A", NegationLawTransformer.apply_law(expression_tree))
    
    def test_uneven_negation(self):
        postfix = InfixToPostfixConverter.attempt_conversion("(¬(¬(¬(¬(¬A)))))")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.law_description + "(¬A)", NegationLawTransformer.apply_law(expression_tree))
    
    def test_other_negation_law1(self):
        postfix = InfixToPostfixConverter.attempt_conversion("(¬(A→B))")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.law_description + "(A∧(¬B))", NegationLawTransformer.apply_law(expression_tree))

    def test_other_negation_law2(self):
        postfix = InfixToPostfixConverter.attempt_conversion("(¬(A↔B))")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.law_description + "(A↔(¬B))", NegationLawTransformer.apply_law(expression_tree))


if __name__ == '__main__':
    unittest.main()