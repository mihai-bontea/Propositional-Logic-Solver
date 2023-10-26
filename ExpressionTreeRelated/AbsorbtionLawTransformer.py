from .LawTransformerBase import LawTransformerBase
from .LogicOperators import *

class ReturnStruct:
    def __init__(self, node, left_child_str="", right_child_str="") -> None:
        self._node = node
        self._left_child_str = left_child_str
        self._right_child_str = right_child_str
    
    @property
    def node(self):
        return self._node
    
    @property
    def left_child_str(self):
        return self._left_child_str
    
    @property
    def right_child_str(self):
        return self._right_child_str
    
    def get_resulting_str(self) -> str:
        if self.node.value in CONNECTIVES:
            return '({}{}{})'.format(self.left_child_str, self.node.value, self.right_child_str)
        elif self.node.value == NEG:
            return '({}{})'.format(NEG, self.left_child_str)
        return self.node.value
    

class AbsorbtionLawTransformer(LawTransformerBase):
    law_description = "Applying absorbtion laws: F {} (F {} G) ~ F, F {} (F {} G) ~ F".\
        format(DISJ, CONJ, CONJ, DISJ)
    
    def apply_law(expression_tree)->str:
        prev_str = expression_tree.inorder_parentheses()

        root_info = AbsorbtionLawTransformer.apply_absorbtion(expression_tree.root)
        expression_tree.root = root_info.node
        result_str = root_info.get_resulting_str()

        if prev_str != result_str:
            return "{}\n{}".format(AbsorbtionLawTransformer.law_description, result_str)
        return ""

    @staticmethod
    def apply_absorbtion(node):
        # Binary connectives
        if node.value in CONNECTIVES:
            left_child_info = AbsorbtionLawTransformer.apply_absorbtion(node.left)
            node.left = left_child_info.node
            str_left = left_child_info.get_resulting_str()

            right_child_info = AbsorbtionLawTransformer.apply_absorbtion(node.right)
            node.right = right_child_info.node
            str_right = right_child_info.get_resulting_str()

            if node.value in (DISJ, CONJ):
                if len(str_left) < len(str_right):
                    if node.right.value in (DISJ, CONJ) and node.value != node.right.value:
                        # check if str_left is 'half' the str_right expression
                        if AbsorbtionLawTransformer.is_operand_of(str_left, right_child_info):
                            return left_child_info

                elif len(str_right) < len(str_left):
                    if node.left.value in (DISJ, CONJ) and node.value != node.left.value:
                        # check if str_right is 'half' the str_left expression
                        if AbsorbtionLawTransformer.is_operand_of(str_right, left_child_info):
                            return right_child_info

            return ReturnStruct(node, str_left, str_right)
        
        # Negation
        elif node.value == NEG:
            left_child_info = AbsorbtionLawTransformer.apply_absorbtion(node.left)
            node.left = left_child_info.node
            str_left = left_child_info.get_resulting_str()
            return ReturnStruct(node, str_left)
        # Atom
        else:
            return ReturnStruct(node)
    
    @staticmethod
    def is_operand_of(
        smaller_exp: str,
        larger_exp: ReturnStruct
        ) -> bool:
        return smaller_exp == larger_exp.left_child_str or smaller_exp == larger_exp.right_child_str
