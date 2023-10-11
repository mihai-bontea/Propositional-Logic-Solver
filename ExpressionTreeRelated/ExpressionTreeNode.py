from LogicOperators import *

class ExpressionTreeNode: 
    def __init__(self , value):
        self.value = value 
        self.left = None
        self.right = None
    
    def inorder_parentheses(self):
        if self.value in CONNECTIVES:
            return '({}{}{})'.format(self.left.inorder_parentheses(), self.value, self.right.inorder_parentheses())
        elif self.value == NEG:
            return '({}{})'.format(NEG, self.left.inorder_parentheses())
        return self.value
    
    def evaluate(self, value_dict):
        # Leaf : operand
        if self.right == self.left == None:
            return value_dict[self.value]
        else:
            # Operator: negation
            if self.value == NEG:
                truth_val = self.left.evaluate(value_dict)
                return OPERATOR_TO_FUNCT[self.value](truth_val) 
                            
            # Operator: other binary connective
            else:
                truth_val1 = self.left.evaluate(value_dict)
                truth_val2 = self.right.evaluate(value_dict)
                return OPERATOR_TO_FUNCT[self.value](truth_val1, truth_val2)
    
    def deep_copy(self):
        new_node = ExpressionTreeNode(self.value)
        new_node.left = None if self.left == None else self.left.deep_copy()
        new_node.right = None if self.right == None else self.right.deep_copy()
        return new_node
