from LawTransformerBase import LawTransformerBase
from ExpressionTree import ExpressionTree
from ExpressionTreeNode import ExpressionTreeNode
from LogicOperators import *

class DeMorganLawTransformer(LawTransformerBase):
    law_description = "Applying De Morgan's laws: {}(F {} G) ~ {}F {} {}G, {}(F {} G) ~ {}G {} {}F".\
        format(NEG, DISJ, NEG, CONJ, NEG, NEG, CONJ, NEG, DISJ, NEG)

    def apply_law(expression_tree : ExpressionTree)->str:
        prev_str = expression_tree.inorder_parentheses()
        expression_tree.root = DeMorganLawTransformer.apply_de_morgan(expression_tree.root)
        # expression_tree.root = DeMorganLawTransformer.apply_de_morgan(expression_tree.root)
        result_str = expression_tree.inorder_parentheses()

        if prev_str != result_str:
            return "{}\n{}".format(DeMorganLawTransformer.law_description, result_str)
        return ""
    @staticmethod
    def apply_de_morgan(node):
        # Binary operator
        if node.value in CONNECTIVES:
            node.left = DeMorganLawTransformer.apply_de_morgan(node.left)
            node.right = DeMorganLawTransformer.apply_de_morgan(node.right)
            return node
        # Negation
        elif node.value == NEG:
            node.left = DeMorganLawTransformer.apply_de_morgan(node.left)

            if node.left.value == DISJ or node.left.value == CONJ:
                # Flip the connective
                node.left.value = CONJ if node.left.value == DISJ else DISJ

                # Creating nodes containing negation
                new_left = ExpressionTreeNode(NEG)
                new_right = ExpressionTreeNode(NEG)

                # Setting children of negations
                new_left.left = node.left.left
                new_right.left = node.left.right

                # Updating the children of the former disjunction
                node.left.left = new_left
                node.left.right = new_right

                return node.left
            # Else, node remains unchanged
            return node

        # Atom
        else:
            return node
        