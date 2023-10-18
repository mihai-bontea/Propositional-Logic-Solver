import unittest
from InfixToPostfix import InfixToPostfixConverter
from ExpressionTree import ExpressionTree
from ConversionTautologies import TautologiesConverter

class TestIdempocyLawTransformer(unittest.TestCase):

    def setUp(self):
        self.CNF_description = "Applying A ∨ (B ∧ C) ~ (A ∨ B) ∧ (A ∨ C) to reach CNF\n"
        self.DNF_description = "Applying A ∧ (B ∨ C) ~ (A ∧ B) ∨ (A ∧ C) to reach DNF\n"

    def tearDown(self):
        pass

    def test_no_change(self):
        postfix = InfixToPostfixConverter.attempt_conversion("¬((A→B)→C)∧D")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual("", TautologiesConverter.apply(expression_tree, '∨', '∧'))
    
    def test_conj_primary(self):
        postfix = InfixToPostfixConverter.attempt_conversion("F∨(G∧H)")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.CNF_description + "((F∨G)∧(F∨H))", TautologiesConverter.apply(expression_tree, '∧', '∨'))
    
    def test_disj_primary(self):
        postfix = InfixToPostfixConverter.attempt_conversion("F∧(G∨H)")
        expression_tree = ExpressionTree(postfix)
        self.assertEqual(self.DNF_description + "((F∧G)∨(F∧H))", TautologiesConverter.apply(expression_tree, '∨', '∧'))


if __name__ == '__main__':
    unittest.main()