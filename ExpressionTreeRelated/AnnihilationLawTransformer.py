from LawTransformerBase import LawTransformerBase
from ExpressionTree import ExpressionTree
from ExpressionTreeNode import ExpressionTreeNode
from LogicOperators import *

class AnnihilationLawTransformer(LawTransformerBase):
    law_description = "Applying annihilation laws: F {} {}F ~ {}, F {} {}F ~ {}, F {} F ~ {}".\
        format(DISJ, NEG, TOP, CONJ, NEG, BOT, IMPL, TOP)
    
    def apply_law(expression_tree : ExpressionTree)->str:
        prev_str = expression_tree.inorder_parentheses()
        expression_tree.root, result_str = AnnihilationLawTransformer.apply_annihilation(expression_tree.root)

        if prev_str != result_str:
            return "{}\n{}".format(AnnihilationLawTransformer.law_description, result_str)
        return ""

    @staticmethod
    def apply_annihilation(node):
        # Binary connectives
        if node.value in CONNECTIVES:
            node.left, str_left = AnnihilationLawTransformer.apply_annihilation(node.left)
            node.right, str_right = AnnihilationLawTransformer.apply_annihilation(node.right)
            
            # Implication with same value on both sides
            if node.value == IMPL and str_left == str_right:
                return ExpressionTreeNode(TOP), TOP
            # Conjunction with complementary values
            if node.value == CONJ and AnnihilationLawTransformer.is_negation_of(str_left, str_right):
                return ExpressionTreeNode(BOT), BOT
            # Disjunction with complementary values
            if node.value == DISJ and AnnihilationLawTransformer.is_negation_of(str_left, str_right):
                return ExpressionTreeNode(TOP), TOP
            
            # Else, leave the node unchanged
            return node, '({}{}{})'.format(str_left, node.value, str_right)

        # Unary connective
        elif node.value == NEG:
            node.left, str_left = AnnihilationLawTransformer.apply_annihilation(node.left)
            return node, '({}{})'.format(NEG, str_left)
        # Atom
        else:
            return node, node.value
    
    @staticmethod
    def is_negation_of(str_left, str_right):
        if len(str_left) > len(str_right):
            str_left, str_right = str_right, str_left

        return str_right == '({}{})'.format(NEG, str_left)
