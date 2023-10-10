import unittest
from InfixToPostfix import InfixToPostfixConverter
from ExpressionTree import ExpressionTree
from TrueFalseLawTransformer import TrueFalseLawTransformer

class TestTrueFalseLawTransformer(unittest.TestCase):

    def setUp(self):
        self.law_description = "Applying laws of 'True' and 'False':\n"

    def tearDown(self):
        pass

    def test_even_negation(self):
        postfix = InfixToPostfixConverter.attempt_conversion("(¬(¬(¬(¬⊤))))")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.law_description + "⊤", TrueFalseLawTransformer.apply_law(expression_tree))

    def test_uneven_negation(self):
        postfix = InfixToPostfixConverter.attempt_conversion("(¬(¬(¬⊤)))")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.law_description + "⊥", TrueFalseLawTransformer.apply_law(expression_tree))

    def test_disjunction_bot_transform(self):
        postfix = InfixToPostfixConverter.attempt_conversion("(((¬F)∧(¬G))∨⊥)")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.law_description + "((¬F)∧(¬G))", TrueFalseLawTransformer.apply_law(expression_tree))

        postfix = InfixToPostfixConverter.attempt_conversion("(⊥∨((¬F)∧(¬G)))")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.law_description + "((¬F)∧(¬G))", TrueFalseLawTransformer.apply_law(expression_tree))

    def test_disjunction_top_transform(self):
        postfix = InfixToPostfixConverter.attempt_conversion("(((¬F)∧(¬G))∨⊤)")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.law_description + "⊤", TrueFalseLawTransformer.apply_law(expression_tree))

        postfix = InfixToPostfixConverter.attempt_conversion("(⊤∨((¬F)∧(¬G)))")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.law_description + "⊤", TrueFalseLawTransformer.apply_law(expression_tree))
    
    def test_conjunction_bot_transform(self):
        postfix = InfixToPostfixConverter.attempt_conversion("(((¬F)∧(¬G))∧⊥)")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.law_description + "⊥", TrueFalseLawTransformer.apply_law(expression_tree))

        postfix = InfixToPostfixConverter.attempt_conversion("(⊥∧((¬F)∧(¬G)))")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.law_description + "⊥", TrueFalseLawTransformer.apply_law(expression_tree))
    
    def test_conjunction_top_transform(self):
        postfix = InfixToPostfixConverter.attempt_conversion("(((¬F)∧(¬G))∧⊤)")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.law_description + "((¬F)∧(¬G))", TrueFalseLawTransformer.apply_law(expression_tree))

        postfix = InfixToPostfixConverter.attempt_conversion("(⊤∧((¬F)∧(¬G)))")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.law_description + "((¬F)∧(¬G))", TrueFalseLawTransformer.apply_law(expression_tree))

    def test_implication_transform(self):
        postfix = InfixToPostfixConverter.attempt_conversion("(⊥→((¬F)∧(¬G)))")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.law_description + "⊤", TrueFalseLawTransformer.apply_law(expression_tree))

        postfix = InfixToPostfixConverter.attempt_conversion("(((¬F)∧(¬G))→⊤)")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.law_description + "⊤", TrueFalseLawTransformer.apply_law(expression_tree))


if __name__ == '__main__':
    unittest.main()