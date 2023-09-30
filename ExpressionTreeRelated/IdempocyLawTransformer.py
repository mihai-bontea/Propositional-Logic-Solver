from LawTransformerBase import LawTransformerBase
from ExpressionTree import ExpressionTree
from LogicOperators import *

class IdempocyLawTransformer(LawTransformerBase):
    law_description = "Applying idempocy laws: F{}F ~ F, F{}F ~ F".format(DISJ, CONJ)
    
    def apply_law(expression_tree : ExpressionTree)->str:
        prev_str = expression_tree.inorder_parentheses()
        expression_tree.root, result_str = IdempocyLawTransformer.apply_idempocy(expression_tree.root)

        if prev_str != result_str:
            return "{}\n{}".format(IdempocyLawTransformer.law_description, result_str)
        return ""

    @staticmethod
    def apply_idempocy(node):
        # Binary connectives
        if node.value in CONNECTIVES:
            node.left, str_left = IdempocyLawTransformer.apply_idempocy(node.left)
            node.right, str_right = IdempocyLawTransformer.apply_idempocy(node.right)
            # Disjunction/Conjunction with same expression on each side => Apply idempocy
            if (node.value == DISJ or node.value == CONJ) and str_left == str_right:
                return node.left, str_left
            # Else, leave the node unchanged
            return node, '({}{}{})'.format(str_left, node.value, str_right)

        # Unary connective
        elif node.value == NEG:
            node.left, str_left = IdempocyLawTransformer.apply_idempocy(node.left)
            return node, '({}{})'.format(NEG, str_left)
        # Atom
        else:
            return node, node.value