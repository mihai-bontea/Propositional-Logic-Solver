import sys
import unittest
sys.stdout.reconfigure(encoding='utf-8')

from Controller import Controller
from Controller import ConversionType
from Controller import ResolutionType
from ExpressionTreeRelated.LogicOperators import *

class TestController(unittest.TestCase):

    def setUp(self):
        self.controller = Controller()
        self.whitelist_nnf = [NEG, CONJ, DISJ, TOP, BOT, ')', '(']

    def tearDown(self):
        pass

    def contains_invalid_characters(self, text, whitelist=()):
        return any(not c.isalpha() and c not in whitelist for c in text)

    def test_convert_invalid_expression(self):
        # Improperly closed parantheses
        expression = "(A∨(B∧A↔(C→⊤)"

        # No matter which normal form we're converting towards, the process should fail
        steps_str_list = self.controller.convert_to_normal_forms(expression, ConversionType.NNF)
        self.assertTrue(isinstance(steps_str_list, Exception))

        steps_str_list = self.controller.convert_to_normal_forms(expression, ConversionType.CNF)
        self.assertTrue(isinstance(steps_str_list, Exception))

        steps_str_list = self.controller.convert_to_normal_forms(expression, ConversionType.DNF)
        self.assertTrue(isinstance(steps_str_list, Exception))


    def test_convert_to_nnf(self):
        expression = "(A∨(B∧A))↔(C→⊤)"
        steps_str_list = self.controller.convert_to_normal_forms(expression, ConversionType.NNF)
        # If something went wrong, the function could return Exception, but the input given is valid
        self.assertFalse(isinstance(steps_str_list, Exception))
        
        # In order for an expression to be a valid NNF expression, it needs to only contain negation,
        # conjunction, disjunction, top, or bottom characters
        _, final_nnf_expression = steps_str_list[-1].split('\n')
        self.assertFalse(self.contains_invalid_characters(final_nnf_expression, self.whitelist_nnf))
        # To be more specific in this case, the expression should simplify down to 'A'
        self.assertEqual(final_nnf_expression, "A")
    
    def test_convert_to_cnf(self):
        expression = "(A∨(B∧A))↔(C→⊤)∧(¬A∨(B∧A))↔(¬C→⊤)"
        steps_str_list = self.controller.convert_to_normal_forms(expression, ConversionType.CNF)
        # If something went wrong, the function could return Exception, but the input given is valid
        self.assertFalse(isinstance(steps_str_list, Exception))
        
        _, final_cnf_expression = steps_str_list[-1].split('\n')
        # print(final_cnf_expression)
        self.assertFalse(self.contains_invalid_characters(final_cnf_expression, self.whitelist_nnf))
    
    def test_convert_to_dnf(self):
        expression = "(A∨(B∧A))↔(C→⊤)∧(¬A∨(B∧A))↔(¬C→⊤)"
        steps_str_list = self.controller.convert_to_normal_forms(expression, ConversionType.DNF)
        # If something went wrong, the function could return Exception, but the input given is valid
        self.assertFalse(isinstance(steps_str_list, Exception))
        
        _, final_dnf_expression = steps_str_list[-1].split('\n')
        # print(final_dnf_expression)
        self.assertFalse(self.contains_invalid_characters(final_dnf_expression, self.whitelist_nnf))

    def test_dpll(self):
        pass