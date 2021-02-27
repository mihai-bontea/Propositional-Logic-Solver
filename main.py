from InfixToPostfix import Conversion
from ExpressionTree import ExpressionTree
import copy

class WFPropositionalFormula:

    def __init__(self, from_str):
        
        # This class variable will store the string of the expression
        self.__expression = copy.deepcopy(from_str)
        self.__expression_tree = None
        self.__postfix = ""

    def is_WFF(self):
        """
        Wrapper function: calls infix_to_postfix which converts the string to postfix form while also
        checking whether it is a WFF
        """
        obj = Conversion() 
        postfix = obj.infix_to_postfix_check(self.__expression)
        if postfix != False:
            self.__postfix = postfix
            print("String is a WFF!")
            return True
        return False

    def store_as_exp_tree(self):
        self.__expression_tree = ExpressionTree(self.__postfix)
        #self.__expression_tree.inorder_traversal()
        return True
    
    def compute_truth_value(self, value_dict):
        """
        Computes the truth value of the proposition under the interpretation given by the
        dictionary value_dict
        """
        self.__expression_tree.comp_truth_value(value_dict, True)
    
    def proposition_type(self, atoms):
        """
        Uses the utility function __back generate all possible interpretations for a
        proposition, then computes the truth value of the proposition with respect to those
        interpretations, in order to determine whether it's a tautology/satisfiable/inconsistent
        """   

        self.__interpretations = []
        self.__atoms = atoms

        self.__back({}, 0)

        all_true = True
        one_true = False

        for intr in self.__interpretations:
            if self.__expression_tree.comp_truth_value(intr, False) == False:
                all_true = False
            else:
                one_true = True
        
        if all_true == True:
            print("The propositional formula given is valid(tautology)!")
        elif one_true == True:
            print("The propositional formula given is satisfiable!")
        else:
            print("The propositional formula given is inconsistent!")

    def __back(self, value_dict, pos):
        """
        Utility function, creates all possible interpretations and stores them into the class variable
        self.__interpretations
        """
        
        if pos == len(self.__atoms):
            obj = copy.deepcopy(value_dict)
            self.__interpretations.append(obj)
        else:

            value_dict[self.__atoms[pos]] = True
            self.__back(value_dict, pos + 1)

            value_dict[self.__atoms[pos]] = False
            self.__back(value_dict, pos + 1)

    def print_exp_tree(self):
        """
        Prints the expression tree associated to the proposition
        """
        if self.__expression_tree != None:
            #self.__expression_tree.inorder_traversal()
            self.__expression_tree.inorder_parentheses()
    
    def convert_to_NNF(self):
        if self.__expression_tree != None:
            self.__expression_tree.convert_to_NNF(True)
    
    def convert_to_DNF(self):
        if self.__expression_tree != None:
            self.__expression_tree.convert_to_DNF()
    
    def convert_to_CNF(self):
        if self.__expression_tree != None:
            self.__expression_tree.convert_to_CNF()