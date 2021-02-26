from COLORS import style 

CONJ = '∧'
DISJ = '∨'
IMPL = '→'
EQUIV = '↔'
NEG = '¬'
TOP = '⊤'
BOT = '⊥'
CONNECTIVES = [EQUIV, IMPL, DISJ, CONJ]

# An expression tree node
class ExpressionTreeNode: 

    # Constructor to create a node 
    def __init__(self , value):
        self.value = value 
        self.left = None
        self.right = None

        # Dictionary which associates to each symbol a function
        self.__funct = {NEG : self.negation, EQUIV: self.equivalence, IMPL : self.implication, DISJ : self.disjunction, CONJ: self.conjunction}
   
    def inorder(self):
        if self.left != None:
            self.left.inorder()

        print (self.value, end = "")
         
        if self.right != None:
            self.right.inorder()
    
    def inorder_parentheses(self):
        
        if self.value in CONNECTIVES:
            string = '(' + self.left.inorder_parentheses() + self.value + self.right.inorder_parentheses() + ')'
            return string
        elif self.value == NEG:
            string = '(¬' + self.left.inorder_parentheses() + ')'
            return string
        else:
            return self.value
    
    def evaluate(self, value_dict, show_steps):
        # Leaf => operand, print its truth value
        if self.right == self.left == None:
            if show_steps == True:
                print("Atom " + self.value + ": " + str(value_dict[self.value]))
            
            return (value_dict[self.value], self.value)

        else:
            # Operator: negation
            if self.value == NEG:
                truth_val, string = self.left.evaluate(value_dict, show_steps)

                negated_truth_val = self.__funct[self.value](truth_val) 
                string = "(" + self.value + string + ")"
                if show_steps == True:
                    print(string + " is " + str(negated_truth_val))
                
                return (negated_truth_val, string)
            
            # Operator: other binary connective
            else:
                truth_val1, string1 = self.left.evaluate(value_dict, show_steps)

                truth_val2, string2 = self.right.evaluate(value_dict, show_steps)

                truth_val = self.__funct[self.value](truth_val1, truth_val2)
                string = "(" + string1 + self.value + string2 + ")"

                if show_steps == True:
                    print(string + " is " + str(truth_val))
                return (truth_val, string)

    @staticmethod
    def negation(truth_val):
        return not truth_val
    
    @staticmethod
    def conjunction(truth_val1, truth_val2):
        return truth_val1 and truth_val2
    
    @staticmethod
    def disjunction(truth_val1, truth_val2):
        return truth_val1 or truth_val2
    
    @staticmethod
    def implication(truth_val1, truth_val2):
        if truth_val1 == True and truth_val2 == False:
            return False
        return True
    
    @staticmethod
    def equivalence(truth_val1, truth_val2):
        return truth_val1 == truth_val2

  
class ExpressionTree:

    def __init__(self, postfix):
        
        self.postfix = postfix 

        self.root = self.__constructTree()
    
    # Returns the root of the constructed tree from the given postfix expression 
    def __constructTree(self): 
        stack = [] 
  
        # Traverse through every character of input expression 
        for char in self.postfix : 
  
            # Operand, simply push into stack 
            if char not in CONNECTIVES and char != NEG: 
                t = ExpressionTreeNode(char) 
                stack.append(t) 
  
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
                    stack.append(t)
                # Char is negation: will only pop 1 operand from the stack
                else:
                    t = ExpressionTreeNode(char)
                    t1 = stack.pop()

                    # Make the operand a child of negation
                    t.left = t1
                    # Add this subexpression to stack
                    stack.append(t)

        # Only element  will be the root of expression tree 
        t = stack.pop() 
     
        return t 

    def convert_to_NNF(self, show_steps):
        
        # Applying the idempocy laws
        self.__idempocy_laws(show_steps)

        # Applying the annihilation laws
        self.__annihilation_laws(show_steps)

        # Applying the laws of true and false
        self.__true_false_laws(show_steps)
        
        # Applying the reduction laws to eliminate equivalences and implications
        self.__reduction_laws(show_steps)

        # Keeps track of whether the loop modifies the formula: we stop when it doesn't
        self.__global_modified_flag = True

        while self.__global_modified_flag == True:
            self.__global_modified_flag = False

            self.__idempocy_laws(show_steps)
            self.__annihilation_laws(show_steps)
            self.__true_false_laws(show_steps)
            self.__negation_laws(show_steps)
        
    """ ###########################################################################
                                Reduction laws functions
    """

    def __reduction_laws(self, show_steps):
        # Initializing the modified flag with False
        self.__modified_flag = False
        self.__reduce_eq_wrapper()
        
        if show_steps == True and self.__modified_flag == True:
            print(style.GREEN("Reducing equivalences: (F↔G) ~ (F→G)∧(G→F)") + style.RESET(""))
            self.inorder_parentheses()

        # Initializing the modified flag with False
        self.__modified_flag = False
        self.__reduce_impl_wrapper()
        
        if show_steps == True and self.__modified_flag == True:
            print(style.GREEN("Reducing implications: (F→G) ~ (¬F∨G)") + style.RESET(""))
            self.inorder_parentheses()

    def __reduce_eq_wrapper(self):
        self.__reduce_eq(self.root)

    def __reduce_eq(self, node):
        
        if node.value == EQUIV:
            # Setting the modified flag to True
            self.__modified_flag = True

            #Changing the node value to '∧'
            node.value = CONJ

            # These will be the new children of the current node
            new_left = ExpressionTreeNode(IMPL)
            new_right = ExpressionTreeNode(IMPL)

            # Setting the children of the new left child of node
            new_left.left = node.left
            new_left.right = node.right

            # Setting the children of the new right child of node
            new_right.left = node.right
            new_right.right = node.left

            # Updating the children of node
            node.left = new_left
            node.right = new_right

            # Call the function for the new left child(will update for right sub-tree too since references)
            self.__reduce_eq(node.left)
        
        else:
            if node.left != None:
                self.__reduce_eq(node.left)
            if node.right != None:
                self.__reduce_eq(node.right)

    def __reduce_impl_wrapper(self):
        self.__reduce_impl(self.root)
    
    def __reduce_impl(self, node):
        if node.value == IMPL:
            # Setting the modified flag to True
            self.__modified_flag = True

            # Changing the node value to '∨'
            node.value = DISJ

            # Creating a new left child for the current node, containing '¬'
            new_left = ExpressionTreeNode(NEG)
            new_left.left = node.left

            # Updating the children of node
            node.left = new_left

        # Call the function for its children
        if node.left != None:
            self.__reduce_impl(node.left)
        if node.right != None:
            self.__reduce_impl(node.right)

    """ ###########################################################################
                                Idempocy laws functions
    """

    def __idempocy_laws(self, show_steps):
        # Initializing the modified flag with False
        self.__modified_flag = False
        self.root, string = self.__apply_idempocy(self.root)

        if show_steps == True and self.__modified_flag == True:
            print(style.GREEN("Applying idempocy laws: F∧F ~ F, F∨F ~ F") + style.RESET(""))
            self.inorder_parentheses()
            self.__global_modified_flag = True

    def __apply_idempocy(self, node):
        str_left = ""
        str_right = ""

        # Binary connectives
        if node.value in CONNECTIVES:
            node.left, str_left = self.__apply_idempocy(node.left)
            node.right, str_right = self.__apply_idempocy(node.right)
        # Unary connective
        elif node.value == NEG:
            node.left, str_left = self.__apply_idempocy(node.left)
        # Atom
        else:
            return (node, node.value)

        # Or / And connective
        if (node.value == DISJ or node.value == CONJ) and str_left == str_right:
            # Return the node containing the child(Apply idempocy)
            # Set the modified flag to True
            self.__modified_flag = True
            return (node.left, str_left)
        elif node.value in CONNECTIVES:
            return (node, '(' + str_left + node.value + str_right + ')')
        elif node.value == NEG:
            return (node, '(' + node.value + str_left + ')')
        else:
            return (node, node.value)

    """ ###########################################################################
                                Annihilation laws functions 
    """

    def __annihilation_laws(self, show_steps):
        # Initializing the modified flag with False
        self.__modified_flag = False
        self.__apply_annihilation(self.root)
        
        if show_steps == True and self.__modified_flag == True:
            print(style.GREEN("Applying annihilation laws: F∨¬F ~ ⊤, F∧¬F ~ ⊥") + style.RESET(""))
            self.inorder_parentheses()
            self.__global_modified_flag = True

    def __apply_annihilation(self, node):
        str_left = ""
        str_right = ""

        # Binary connectives
        if node.value in CONNECTIVES:
            str_left = self.__apply_annihilation(node.left)
            str_right = self.__apply_annihilation(node.right)
        # Unary connective
        elif node.value == NEG:
            str_left = self.__apply_annihilation(node.left)
        # Atom
        else:
            return node.value
        
        # Implication + Annihilation
        if node.value == IMPL and str_left == str_right:
            # Setting the modified flag to True
            self.__modified_flag = True
            # Changing the value of the node to 'T'
            node.value = TOP
            
            # Deleting the children nodes
            node.left = None
            node.right = None

            return node.value
        
        # Disjunction + Annihilation
        elif node.value == DISJ and ('(¬' + str_left + ')' == str_right or str_left == '(¬' + str_right + ')'):
            # Setting the modified flag to True
            self.__modified_flag = True
            # Changing the value of the node to 'T'
            node.value = TOP

            # Deleting the children nodes
            node.left = None
            node.right = None

            return node.value
        
        # Conjunction + Annihilation
        elif node.value == CONJ and ('(¬' + str_left + ')' == str_right or str_left == '(¬' + str_right + ')'):
            # Setting the modified flag to True
            self.__modified_flag = True
            # Changing the value of the node to '⊥'
            node.value = BOT

            # Deleting the children nodes
            node.left = None
            node.right = None

            return node.value
        
        # Binary connective
        elif node.value in CONNECTIVES:
            return '(' + str_left + node.value + str_right + ')'
        # Unary connective(negation)
        elif node.value == NEG:
            return '(' + node.value + str_left + ')'
        # Atom
        else:
            return node.value
    
    """ ###########################################################################
                                Laws of True and False functions
    """

    def __true_false_laws(self, show_steps):
        # Initializing the modified flag with False
        self.__modified_flag = False
        self.root = self.__apply_true_false(self.root)

        if show_steps == True and self.__modified_flag == True:
            print(style.GREEN("Applying laws of 'True' and 'False': ") + style.RESET(""))
            self.inorder_parentheses()
            self.__global_modified_flag = True

    def __apply_true_false(self, node):
        
        # Binary connective
        if node.value in CONNECTIVES:
            node.left = self.__apply_true_false(node.left)
            node.right = self.__apply_true_false(node.right)
        
        # Unary connective
        elif node.value == NEG:
            node.left = self.__apply_true_false(node.left)
        # Atom
        else:
            return node

        # Negation
        if node.value == NEG:
            if node.left.value == TOP:
                # Setting the modified flag to True
                self.__modified_flag = True
                node.value = BOT
                node.left = None
                return node
            elif node.left.value == BOT:
                # Setting the modified flag to True
                self.__modified_flag = True
                node.value = TOP
                node.left = None
                return node
        # Disjunction
        elif node.value == DISJ:
            if node.left.value == BOT:
                # Setting the modified flag to True
                self.__modified_flag = True
                return node.right
            elif node.right.value == BOT:
                # Setting the modified flag to True
                self.__modified_flag = True 
                return node.left
            elif node.left.value == TOP:
                # Setting the modified flag to True
                self.__modified_flag = True
                return node.left
            elif node.right.value == TOP:
                # Setting the modified flag to True
                self.__modified_flag = True
                return node.right
        # Conjunction
        elif node.value == CONJ:
            if node.left.value == TOP:
                # Setting the modified flag to True
                self.__modified_flag = True
                return node.right
            elif node.right.value == TOP:
                # Setting the modified flag to True
                self.__modified_flag = True
                return node.left
            elif node.left.value == BOT:
                # Setting the modified flag to True
                self.__modified_flag = True
                return node.left
            elif node.right.value == BOT:
                # Setting the modified flag to True
                self.__modified_flag = True
                return node.right
        # Implication
        elif node.value == IMPL and (node.left.value == BOT or node.right.value == TOP):
            if node.left.value == BOT:
                # Setting the modified flag to True
                self.__modified_flag = True
                node.value = TOP
                node.left = None
                return node
        
        return node

    """ ###########################################################################
                                Negation functions
    """

    def __negation_laws(self, show_steps):
        # Initializing the modified flag with False
        self.__modified_flag = False
        self.root = self.__apply_double_negation(self.root)

        if show_steps == True and self.__modified_flag == True:
            print(style.GREEN("Removing double negations: ¬(¬F) ~ F") + style.RESET(""))
            self.inorder_parentheses()
            self.__global_modified_flag = True

        # Initializing the modified flag with False
        self.__modified_flag = False
        self.root = self.__apply_de_morgan(self.root)
        
        if show_steps == True and self.__modified_flag == True:
            print(style.GREEN("Applying De Morgan's laws: ¬(F∨G) ~ ¬F∧¬G, ¬(F∧G) ~ ¬G∨¬F") + style.RESET("")) 
            self.inorder_parentheses()
            self.__global_modified_flag = True

        # Initializing the modified flag with False
        self.__modified_flag = False
        self.root = self.__apply_other_negation(self.root)

        if show_steps == True and self.__modified_flag == True:
            print(style.GREEN("Applying other negations: ¬(F→G) ~ F∧(¬G), ¬(F↔G) ~ F↔(¬G)") + style.RESET(""))
            self.inorder_parentheses()
            self.__global_modified_flag = True

    def __apply_de_morgan(self, node):
        # Binary operator
        if node.value in CONNECTIVES:
            node.left = self.__apply_de_morgan(node.left)
            node.right = self.__apply_de_morgan(node.right)
        # Unary operator
        elif node.value == NEG:
            node.left = self.__apply_de_morgan(node.left)
        # Atom
        else:
            return node
        
        if node.value == NEG:
    
            if node.left.value == DISJ or node.left.value == CONJ:
                # Set the modified flag to True
                self.__modified_flag = True

                # Flip the connective
                if node.left.value == DISJ:
                    node.left.value = CONJ
                else:
                    node.left.value = DISJ

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
        
        return node

    def __apply_other_negation(self, node):
        # Binary operator
        if node.value in CONNECTIVES:
            node.left = self.__apply_other_negation(node.left)
            node.right = self.__apply_other_negation(node.right)
        # Unary operator
        elif node.value == NEG:
            node.left = self.__apply_other_negation(node.left)
        # Atom
        else:
            return node
        
        if node.value == NEG:
        
            if node.left.value == IMPL or node.left.value == EQUIV:
                # Set the modified flag to True
                self.__modified_flag = True

                # Flip the connective in the case of implication
                if node.left.value == IMPL:
                    node.left.value = CONJ

                # Creating a new node containig negation
                new_right = ExpressionTreeNode(NEG)

                # Setting child of negation
                new_right.left = node.left.right

                # Updating the child of the former implication/equivalence
                node.left.right = new_right

                return node.left
        
        return node
        
    def __apply_double_negation(self, node):
        
        # Negation
        if node.value == NEG:

            count = 1
            current_node = node

            # Reaching the last negation in the tree, and counting their amount
            while current_node.left.value == NEG:
                count += 1
                current_node = current_node.left
            
            if count > 1:
                # Set the modified flag to True
                self.__modified_flag = True

            # Recur down the tree first
            current_node.left = self.__apply_double_negation(current_node.left)

            # If there is an even amount of negations, return the child of the last negation
            if count % 2 == 0:
                return current_node.left
            # Else return the last negation in the subtree
            else:
                return current_node

        # Other binary connectives
        elif node.value in CONNECTIVES:
            node.left = self.__apply_double_negation(node.left)
            node.right = self.__apply_double_negation(node.right)
        # Atoms
        return node

    """ ########################################################################### """

    def convert_to_DNF(self):
        # Initializing the modified flag with False
        self.__modified_flag = False
        self.root = self.__apply_tautologies(self.root, CONJ, DISJ)
        if self.__modified_flag == True:
            print(style.GREEN("Applying A∧(B∨C) ~ (A∧B)∨(A∧C) to reach DNF") + style.RESET(""))
            self.inorder_parentheses()
        else:
            print(style.RED("No more modifications required to reach DNF.") + style.RESET(""))

    def convert_to_CNF(self):
        # Initializing the modified flag with False
        self.__modified_flag = False
        self.root = self.__apply_tautologies(self.root, DISJ, CONJ)
        if self.__modified_flag == True:
            print(style.GREEN("Applying A∨(B∧C) ~ (A∨B)∧(A∨C) to reach CNF") + style.RESET(""))
            self.inorder_parentheses()
        else:
            print(style.RED("No more modifications required to reach CNF.") + style.RESET(""))

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

    def inorder_traversal(self):
        if self.root != None:
            self.root.inorder()
    
    def inorder_parentheses(self):
        if self.root != None:
            print(style.CYAN(self.root.inorder_parentheses()) + style.RESET(""))

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

def test():
    et = ExpressionTree("A¬CD∧∨A¬∨")
    et.inorder_traversal()

#test() 