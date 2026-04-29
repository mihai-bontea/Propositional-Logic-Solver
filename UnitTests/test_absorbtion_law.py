import unittest
from ExpressionTreeRelated.InfixToPostfix import InfixToPostfixConverter
from ExpressionTreeRelated.ExpressionTree import ExpressionTree
from ExpressionTreeRelated.AbsorbtionLawTransformer import AbsorbtionLawTransformer

class TestAbsorbtionLawTransformer(unittest.TestCase):

    def setUp(self):
        self.law_description = "Applying absorbtion laws: F ∨ (F ∧ G) ~ F, F ∧ (F ∨ G) ~ F\n"

    def tearDown(self):
        pass

    def test_no_change(self):
        postfix = InfixToPostfixConverter.attempt_conversion("¬((A→B)→C)∧D")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual("", AbsorbtionLawTransformer.apply_law(expression_tree))
    
    def test_disj_conj_change(self):
        postfix = InfixToPostfixConverter.attempt_conversion("(F∨(F∧G))")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.law_description + "F", AbsorbtionLawTransformer.apply_law(expression_tree))
    
    def test_disj_conj_change_mirrored(self):
        postfix = InfixToPostfixConverter.attempt_conversion("((F∧G)∨F)")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.law_description + "F", AbsorbtionLawTransformer.apply_law(expression_tree))
    
    def test_conj_disj_change(self):
        postfix = InfixToPostfixConverter.attempt_conversion("(F∧(F∨G))")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.law_description + "F", AbsorbtionLawTransformer.apply_law(expression_tree))
    
    def test_conj_disj_change_mirrored(self):
        postfix = InfixToPostfixConverter.attempt_conversion("((F∨G)∧F)")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.law_description + "F", AbsorbtionLawTransformer.apply_law(expression_tree))
    
    def test_negated_conj_disj_change(self):
        postfix = InfixToPostfixConverter.attempt_conversion("((¬F)∧((¬F)∨G))")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.law_description + "(¬F)", AbsorbtionLawTransformer.apply_law(expression_tree))
    
    def test_special_case_disj(self):
        postfix = InfixToPostfixConverter.attempt_conversion("A∨(A∨B)")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.law_description + "(A∨B)", AbsorbtionLawTransformer.apply_law(expression_tree))
    
    def test_special_case_disj_mirrored(self):
        postfix = InfixToPostfixConverter.attempt_conversion("(B∨A)∨A")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.law_description + "(B∨A)", AbsorbtionLawTransformer.apply_law(expression_tree))

    def test_special_case_conj(self):
        postfix = InfixToPostfixConverter.attempt_conversion("A∧(A∧B)")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.law_description + "(A∧B)", AbsorbtionLawTransformer.apply_law(expression_tree))
    
    def test_special_case_conj_mirrored(self):
        postfix = InfixToPostfixConverter.attempt_conversion("(B∧A)∧A")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.law_description + "(B∧A)", AbsorbtionLawTransformer.apply_law(expression_tree))
    

if __name__ == '__main__':
    unittest.main()