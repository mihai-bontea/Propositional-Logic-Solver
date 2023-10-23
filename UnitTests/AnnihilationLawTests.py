import unittest
from InfixToPostfix import InfixToPostfixConverter
from ExpressionTree import ExpressionTree
from AnnihilationLawTransformer import AnnihilationLawTransformer

class TestAnnihilationLawTransformer(unittest.TestCase):

    def setUp(self):
        self.law_description = "Applying annihilation laws: F ∨ ¬F ~ ⊤, F ∧ ¬F ~ ⊥, F → F ~ ⊤\n"

    def tearDown(self):
        pass

    def test_no_change(self):
        postfix = InfixToPostfixConverter.attempt_conversion("¬((A→B)→C)∧D")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual("", AnnihilationLawTransformer.apply_law(expression_tree))

    def test_simple_disjunction_change(self):
        postfix = InfixToPostfixConverter.attempt_conversion("¬A∨A")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.law_description + "⊤", AnnihilationLawTransformer.apply_law(expression_tree))

    def test_simple_conjunction_change(self):
        postfix = InfixToPostfixConverter.attempt_conversion("A∧¬A")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.law_description + "⊥", AnnihilationLawTransformer.apply_law(expression_tree))
    
    def test_expression(self):
        postfix = InfixToPostfixConverter.attempt_conversion("¬((A∧B)∨¬(A∧B))∨((A∧B)∨¬(A∧B))")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.law_description + "⊤", AnnihilationLawTransformer.apply_law(expression_tree))

if __name__ == '__main__':
    unittest.main()