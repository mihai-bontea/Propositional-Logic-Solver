from ExpressionTreeNode import ExpressionTreeNode
from LogicOperators import *
from Stack import Stack

class ExpressionTree:

    def __init__(self, postfix):
        self.postfix = postfix 
        self.root = self.__constructTree()
    
    # Returns the root of the constructed tree from the given postfix expression 
    def __constructTree(self): 
        # stack = []
        stack = Stack() 
  
        # Traverse through every character of input expression 
        for char in self.postfix : 
  
            # Operand, simply push into stack 
            if char not in CONNECTIVES and char != NEG: 
                t = ExpressionTreeNode(char) 
                # stack.append(t)
                stack.push(t) 
  
            # Operator 
            else: 
                
                # Char is a connective different from negation(unary operator)
                if char in CONNECTIVES:
                    # Pop two top nodes 
                    t = ExpressionTreeNode(char) 
                    t1 = stack.pop() 
                    t2 = stack.pop() 
                
                    # make them children 
                    t.right = t1 
                    t.left = t2 
              
                    # Add this subexpression to stack 
                    # stack.append(t)
                    stack.push(t)
                # Char is negation: will only pop 1 operand from the stack
                else:
                    t = ExpressionTreeNode(char)
                    t1 = stack.pop()

                    # Make the operand a child of negation
                    t.left = t1
                    # Add this subexpression to stack
                    # stack.append(t)
                    stack.push(t)

        # Only element  will be the root of expression tree 
        t = stack.pop() 
     
        return t 

    def convert_to_NNF(self, show_steps):
        
        # Applying the idempocy laws
        # self.__idempocy_laws(show_steps)

        # Applying the annihilation laws
        # self.__annihilation_laws(show_steps)

        # Applying the laws of true and false
        # self.__true_false_laws(show_steps)
        
        # Applying the reduction laws to eliminate equivalences and implications
        self.__reduction_laws(show_steps)

        # Keeps track of whether the loop modifies the formula: we stop when it doesn't
        self.__global_modified_flag = True

        # TODO: we might miss to do some needed changes because last law didn't happen(each law sets the flag to false
        # at the beginning)
        while self.__global_modified_flag == True:
            self.__global_modified_flag = False

            # self.__idempocy_laws(show_steps)
            # self.__annihilation_laws(show_steps)
            # self.__true_false_laws(show_steps)
            self.__negation_laws(show_steps)
        
    """ ###########################################################################
                                Reduction laws functions
    """

    def __reduction_laws(self, show_steps):
        # Initializing the modified flag with False
        self.__modified_flag = False
        # self.__reduce_eq_wrapper()
        
        if show_steps == True and self.__modified_flag == True:
            # print(style.GREEN("Reducing equivalences: (F↔G) ~ (F→G)∧(G→F)") + style.RESET(""))
            self.inorder_parentheses()

        # Initializing the modified flag with False
        self.__modified_flag = False
        # self.__reduce_impl_wrapper()
        
        if show_steps == True and self.__modified_flag == True:
            # print(style.GREEN("Reducing implications: (F→G) ~ (¬F∨G)") + style.RESET(""))
            self.inorder_parentheses()
 
    """ ########################################################################### """

    def convert_to_DNF(self):
        # Initializing the modified flag with False
        self.__modified_flag = False
        self.root = self.__apply_tautologies(self.root, CONJ, DISJ)
        if self.__modified_flag == True:
            # print(style.GREEN("Applying A∧(B∨C) ~ (A∧B)∨(A∧C) to reach DNF") + style.RESET(""))
            self.inorder_parentheses()
        else:
            # print(style.RED("No more modifications required to reach DNF.") + style.RESET(""))
            pass

    def convert_to_CNF(self):
        # Initializing the modified flag with False
        self.__modified_flag = False
        self.root = self.__apply_tautologies(self.root, DISJ, CONJ)
        if self.__modified_flag == True:
            # print(style.GREEN("Applying A∨(B∧C) ~ (A∨B)∧(A∨C) to reach CNF") + style.RESET(""))
            self.inorder_parentheses()
        else:
            # print(style.RED("No more modifications required to reach CNF.") + style.RESET(""))
            pass

    def __apply_tautologies(self, node, primary, secondary):
        
        if node.left != None:
            node.left = self.__apply_tautologies(node.left, primary, secondary)
        if node.right != None:
            node.right = self.__apply_tautologies(node.right, primary, secondary)

        if node.value == primary and (node.left != None and node.left.value == secondary):
            self.__modified_flag = True
            # Changing the value of node.value 
            node.value = secondary

            # Save the node.left.right
            temp = node.left.right

            # Changing the value of node.left.value 
            node.left.value = primary
            node.left.right = node.right

            # Creating a new node
            new_right = ExpressionTreeNode(secondary)
            new_right.left = temp
            new_right.right = node.right

            node.right = new_right

        elif node.value == primary and (node.right != None and node.right.value == secondary):
            self.__modified_flag = True
            # Changing the value of node.value 
            node.value = secondary

            # Save the node.right.right
            temp = node.right.left

            # Changing the value of node.right.value 
            node.right.value = primary
            node.right.left = node.left

            # Creating a new node
            new_left = ExpressionTreeNode(primary)
            new_left.left = node.left
            new_left.right = temp

            node.left = new_left

        return node

    """ ########################################################################### """
    
    def inorder_parentheses(self):
        if self.root != None:
            # print(style.CYAN(self.root.inorder_parentheses()) + style.RESET(""))
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