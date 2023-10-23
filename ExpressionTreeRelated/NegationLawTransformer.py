from .LawTransformerBase import LawTransformerBase
from .ExpressionTreeNode import ExpressionTreeNode
from .LogicOperators import *

class NegationLawTransformer(LawTransformerBase):
    law_description = "Applying negation laws: {}({}F) ~ F, {}(F {} G) ~ F {} ({}G), {}(F {} G) ~ F {} ({}G)".\
        format(NEG, NEG, NEG, IMPL, CONJ, NEG, NEG, EQUIV, EQUIV, NEG)

    def apply_law(expression_tree)->str:
        prev_str = expression_tree.inorder_parentheses()
        expression_tree.root = NegationLawTransformer.apply_double_negation(expression_tree.root)
        expression_tree.root = NegationLawTransformer.apply_other_negation(expression_tree.root)
        result_str = expression_tree.inorder_parentheses()

        if prev_str != result_str:
            return "{}\n{}".format(NegationLawTransformer.law_description, result_str)
        return ""
    
    @staticmethod
    def apply_double_negation(node):
        # Negation
        if node.value == NEG:
            neg_count = 1
            current_node = node

            # Counting the number of consecutive negations
            while current_node.left.value == NEG:
                neg_count += 1
                current_node = current_node.left
            
            # Recur down the tree first
            current_node.left = NegationLawTransformer.apply_double_negation(current_node.left)

            # If there is an even amount of negations, return the child of the last negation
            if neg_count % 2 == 0:
                return current_node.left
            # Else return the last negation in the subtree
            else:
                return current_node
        # Other binary connectives
        elif node.value in CONNECTIVES:
            node.left = NegationLawTransformer.apply_double_negation(node.left)
            node.right = NegationLawTransformer.apply_double_negation(node.right)
        # Atoms
        return node
    
    @staticmethod
    def apply_other_negation(node):
        # Binary operator
        if node.value in CONNECTIVES:
            node.left = NegationLawTransformer.apply_other_negation(node.left)
            node.right = NegationLawTransformer.apply_other_negation(node.right)
            return node
        # Negation
        elif node.value == NEG:
            node.left = NegationLawTransformer.apply_other_negation(node.left)

            if node.left.value == IMPL or node.left.value == EQUIV:
                # Change the connective to conjunction in the case of implication
                if node.left.value == IMPL:
                    node.left.value = CONJ
                
                # Creating a new node containig negation
                new_right = ExpressionTreeNode(NEG)

                # Setting child of negation
                new_right.left = node.left.right

                # Updating the child of the former implication/equivalence
                node.left.right = new_right

                # Eliminating negation
                return node.left
            return node

        # Atom
        else:
            return node
