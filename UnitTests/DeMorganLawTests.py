import unittest
from InfixToPostfix import InfixToPostfixConverter
from ExpressionTree import ExpressionTree
from DeMorganLawTransformer import DeMorganLawTransformer

class TestDeMorganLawTransformer(unittest.TestCase):

    def setUp(self):
        self.law_description = "Applying De Morgan's laws: ¬(F ∨ G) ~ ¬F ∧ ¬G, ¬(F ∧ G) ~ ¬G ∨ ¬F\n"

    def tearDown(self):
        pass

    def test_disj_to_conj(self):
        postfix = InfixToPostfixConverter.attempt_conversion("(¬(F∨G))")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.law_description + "((¬F)∧(¬G))", DeMorganLawTransformer.apply_law(expression_tree))
    
    def test_apply_twice(self):
        postfix = InfixToPostfixConverter.attempt_conversion("(¬(F∨G))")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.law_description + "((¬F)∧(¬G))", DeMorganLawTransformer.apply_law(expression_tree))
        self.assertEqual("", DeMorganLawTransformer.apply_law(expression_tree))

    def test_conj_to_disj(self):
        postfix = InfixToPostfixConverter.attempt_conversion("(¬(F∧G))")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.law_description + "((¬F)∨(¬G))", DeMorganLawTransformer.apply_law(expression_tree))


if __name__ == '__main__':
    unittest.main()