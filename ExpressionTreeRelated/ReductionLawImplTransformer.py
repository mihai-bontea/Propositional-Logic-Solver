from .LawTransformerBase import LawTransformerBase
from .ExpressionTreeNode import ExpressionTreeNode
from .LogicOperators import *

class ReductionLawImplTransformer(LawTransformerBase):
    law_description = "Reducing implications: (F {} G) ~ ({}F {} G)".\
        format(IMPL, NEG, DISJ)

    def apply_law(expression_tree)->str:
        prev_str = expression_tree.inorder_parentheses()
        expression_tree.root = ReductionLawImplTransformer.apply_reduction_for_impl(expression_tree.root)
        result_str = expression_tree.inorder_parentheses()

        if prev_str != result_str:
            return "{}\n{}".format(ReductionLawImplTransformer.law_description, result_str)
        return ""
    
    @staticmethod
    def apply_reduction_for_impl(node):
        # Binary connective
        if node.value in CONNECTIVES:
            node.left = ReductionLawImplTransformer.apply_reduction_for_impl(node.left)
            node.right = ReductionLawImplTransformer.apply_reduction_for_impl(node.right)

            if node.value == IMPL:
                # Changing the node value to DISJ
                node.value = DISJ

                # Creating a new left child for the current node, containing '¬'
                new_left = ExpressionTreeNode(NEG)
                new_left.left = node.left

                # Updating the children of node
                node.left = new_left
        
        elif node.value == NEG:
            node.left = ReductionLawImplTransformer.apply_reduction_for_impl(node.left)
        
        return node