from LogicOperators import *
from ExpressionTreeNode import ExpressionTreeNode

class TautologiesConverter:
    @staticmethod
    def apply(expression_tree, primary, secondary)->str:
        conv_description = "Applying A {} (B {} C) ~ (A {} B) {} (A {} C) to reach {}".\
            format(secondary, primary, secondary, primary, secondary, "CNF" if primary == CONJ else "DNF")
        
        prev_str = expression_tree.inorder_parentheses()
        TautologiesConverter.apply_conversion(expression_tree.root, primary, secondary)
        result_str = expression_tree.inorder_parentheses()

        if prev_str != result_str:
            return "{}\n{}".format(conv_description, result_str)
        return ""

    @staticmethod
    def apply_conversion(node, primary, secondary):
        if node.value == secondary:
            if node.left.value == primary:
                new_right = ExpressionTreeNode(secondary)
                new_right.left = node.left.right
                new_right.right = node.right
                node.right = new_right

                node.value = primary
                node.left.value = secondary

                node.left.right = new_right.right.deep_copy()

            elif node.right.value == primary:
                new_left = ExpressionTreeNode(secondary)
                new_left.left = node.left
                new_left.right = node.right.left
                node.left = new_left

                node.value = primary
                node.right.value = secondary

                node.right.left = new_left.left.deep_copy()

        if node.left != None:
            TautologiesConverter.apply_conversion(node.left, primary, secondary)
        if node.right != None:
            TautologiesConverter.apply_conversion(node.right, primary, secondary)
