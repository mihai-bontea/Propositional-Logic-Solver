from .LawTransformerBase import LawTransformerBase
from .ExpressionTreeNode import ExpressionTreeNode
from .LogicOperators import *

class TrueFalseLawTransformer(LawTransformerBase):
    law_description = "Applying laws of 'True' and 'False':"

    def apply_law(expression_tree)->str:
        prev_str = expression_tree.inorder_parentheses()
        expression_tree.root = TrueFalseLawTransformer.apply_negated_top_or_bot(expression_tree.root)
        expression_tree.root = TrueFalseLawTransformer.apply_true_false_laws(expression_tree.root)
        result_str = expression_tree.inorder_parentheses()

        if prev_str != result_str:
            return "{}\n{}".format(TrueFalseLawTransformer.law_description, result_str)
        return ""
    
    @staticmethod
    def apply_negated_top_or_bot(node):
        # Binary connective
        if node.value in CONNECTIVES:
            node.left = TrueFalseLawTransformer.apply_negated_top_or_bot(node.left)
            node.right = TrueFalseLawTransformer.apply_negated_top_or_bot(node.right)
            return node
        
        # Negation
        elif node.value == NEG:
            node.left = TrueFalseLawTransformer.apply_negated_top_or_bot(node.left)

            if node.left.value == TOP or node.left.value == BOT:
                node.value = TOP if node.left.value == BOT else BOT
                node.left = None
            return node

        # Atom
        else:
            return node
        
    @staticmethod
    def apply_true_false_laws(node):
        # Binary connective
        if node.value in CONNECTIVES:
            node.left = TrueFalseLawTransformer.apply_true_false_laws(node.left)
            node.right = TrueFalseLawTransformer.apply_true_false_laws(node.right)

            if node.value == DISJ:
                if node.left.value == BOT:
                    return node.right
                elif node.right.value == BOT:
                    return node.left
                elif node.left.value == TOP:
                    return node.left
                elif node.right.value == TOP:
                    return node.right
            
            elif node.value == CONJ:
                if node.left.value == TOP:
                    return node.right
                elif node.right.value == TOP:
                    return node.left
                elif node.left.value == BOT:
                    return node.left
                elif node.right.value == BOT:
                    return node.right
                
            elif node.value == IMPL and (node.left.value == BOT or node.right.value == TOP):
                return ExpressionTreeNode(TOP)
            return node

        # Negation
        elif node.value == NEG:
            node.left = TrueFalseLawTransformer.apply_true_false_laws(node.left)
            return node
        # Atom
        else:
            return node