from .ExpressionTreeNode import ExpressionTreeNode
from .LogicOperators import *
from .Stack import Stack

from .AbsorbtionLawTransformer import AbsorbtionLawTransformer
from .AnnihilationLawTransformer import AnnihilationLawTransformer
from .DeMorganLawTransformer import DeMorganLawTransformer
from .IdempocyLawTransformer import IdempocyLawTransformer
from .NegationLawTransformer import NegationLawTransformer
from .ReductionLawEquivTransformer import ReductionLawEquivTransformer
from .ReductionLawImplTransformer import ReductionLawImplTransformer
from .TrueFalseLawTransformer import TrueFalseLawTransformer
from .ConversionTautologies import TautologiesConverter

class ExpressionTree:
    repeating_laws = [AbsorbtionLawTransformer, AnnihilationLawTransformer, IdempocyLawTransformer,
                          NegationLawTransformer, TrueFalseLawTransformer, DeMorganLawTransformer]

    def __init__(self, postfix):
        self.root = self.constructTree(postfix)
    
    # Returns the root of the constructed tree from the given postfix expression 
    def constructTree(self, postfix): 
        stack = Stack() 
  
        # Traverse through every character of input expression 
        for char in postfix : 
            # Operand, simply push into stack 
            if char not in CONNECTIVES and char != NEG: 
                node = ExpressionTreeNode(char) 
                stack.push(node) 
  
            # Operator 
            else: 
                # Char is a connective different from negation(unary operator)
                if char in CONNECTIVES:
                    # Pop two top nodes 
                    node = ExpressionTreeNode(char) 
                    right_child = stack.pop() 
                    left_child = stack.pop() 
                
                    # Set child nodes
                    node.right = right_child
                    node.left = left_child
              
                    # Add this subexpression to stack 
                    stack.push(node)
                # Char is negation: will only pop 1 operand from the stack
                else:
                    node = ExpressionTreeNode(char)
                    left_child = stack.pop()

                    # Make the operand a child of negation
                    node.left = left_child
                    # Add this subexpression to stack
                    stack.push(node)

        # Only element  will be the root of expression tree 
        return stack.pop()

    def apply_repeating_laws(self) -> list:
        steps_str_list = []
        
        expr_changed = True
        while expr_changed:
            expr_changed = False
            for law in ExpressionTree.repeating_laws:
                summary_str = law.apply_law(self)
                if summary_str != "":
                    steps_str_list.append(summary_str)
                    expr_changed = True
        
        return steps_str_list

    def convert_to_NNF(self) -> list:
        steps_str_list = []
        
        # First run of all repeating laws
        steps_str_list.extend(self.apply_repeating_laws())

        # Reducing equivalences
        reduce_equiv_summary = ReductionLawEquivTransformer.apply_law(self)
        if reduce_equiv_summary != "":
            steps_str_list.append(reduce_equiv_summary)
        
        # Second run of all repeating laws
        steps_str_list.extend(self.apply_repeating_laws())

        # Reducing implications
        reduce_impl_summary = ReductionLawImplTransformer.apply_law(self)
        if reduce_impl_summary != "":
            steps_str_list.append(reduce_impl_summary)

        # Last run of all repeating laws
        steps_str_list.extend(self.apply_repeating_laws())

        return steps_str_list

    def convert_to_DNF(self) -> list:
        steps_str_list = self.convert_to_NNF()
        tautologies_summary = TautologiesConverter.apply(self, DISJ, CONJ)
        if tautologies_summary != "":
            steps_str_list.append(tautologies_summary)
        
        return steps_str_list

    def convert_to_CNF(self) -> list:
        steps_str_list = self.convert_to_NNF()
        tautologies_summary = TautologiesConverter.apply(self, CONJ, DISJ)
        if tautologies_summary != "":
            steps_str_list.append(tautologies_summary)
        
        return steps_str_list
    
    def inorder_parentheses(self) -> str:
        if self.root != None:
            return self.root.inorder_parentheses()

    def comp_truth_value(self, value_dict, show_steps):
        """
        Computes the truth value of the expression associated to the expression tree,
        based on 'value_dict', a dictionary which maps each propositional variable to
        a truth value. It also shows the steps
        """
        if self.root != None:
            return self.root.evaluate(value_dict, show_steps)[0]
        else:
            print("Empty expression!")
