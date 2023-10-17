from LawTransformerBase import LawTransformerBase
from ExpressionTreeNode import ExpressionTreeNode
from LogicOperators import *

class ReductionLawEquivTransformer(LawTransformerBase):
    law_description = "Reducing equivalences: (F {} G) ~ (F {} G) {} (G {} F)".\
        format(EQUIV, IMPL, CONJ, IMPL)

    def apply_law(expression_tree)->str:
        prev_str = expression_tree.inorder_parentheses()
        expression_tree.root = ReductionLawEquivTransformer.apply_reduction_for_equiv(expression_tree.root)
        result_str = expression_tree.inorder_parentheses()

        if prev_str != result_str:
            return "{}\n{}".format(ReductionLawEquivTransformer.law_description, result_str)
        return ""
    
    @staticmethod
    def apply_reduction_for_equiv(node):
        # Binary connective
        if node.value in CONNECTIVES:
            node.left = ReductionLawEquivTransformer.apply_reduction_for_equiv(node.left)
            node.right = ReductionLawEquivTransformer.apply_reduction_for_equiv(node.right)
        
            if node.value == EQUIV:
                # Changing the node value to '∧'
                node.value = CONJ

                # New children of the current node
                new_left = ExpressionTreeNode(IMPL)
                new_right = ExpressionTreeNode(IMPL)

                # Setting children of new left child of node
                new_left.left = node.left
                new_left.right = node.right

                # Setting children of new right child of node(must be deep copy)
                new_right.left = node.right.deep_copy()
                new_right.right = node.left.deep_copy()

                # Updating the children of node
                node.left = new_left
                node.right = new_right
            
        elif node.value == NEG:
            node.left = ReductionLawEquivTransformer.apply_reduction_for_equiv(node.left)
        
        return node