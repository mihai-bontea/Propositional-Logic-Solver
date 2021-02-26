CONJ = '∧'
DISJ = '∨'
IMPL = '→'
EQUIV = '↔'
NEG = '¬'
TOP = '⊤'
BOT = '⊥'
CONNECTIVES = [EQUIV, IMPL, DISJ, CONJ]

class Conversion: 
      
    def __init__(self): 
        self.st = [] 
        # Precedence setting 
        self.output = [] 
        self.precedence = {NEG : 5, DISJ : 4, CONJ : 3, IMPL : 2, EQUIV : 1} 
      
    # Returns True if stack is empty, False otherwise
    def __isEmpty(self): 
        return len(self.st) == 0
      
    # Returns the value at the top of the stack
    def __top(self): 
        return self.st[-1] 
      
    # Pops the element from the stack 
    def __pop(self): 
        if not self.__isEmpty(): 
            return self.st.pop() 
      
    # Pushes the element to the stack 
    def __push(self, op): 
        self.st.append(op)  
  
    # Returns True if character is an operand, False otherwise  
    def __isOperand(self, ch): 
        return (ch.isalpha() and ch.isupper()) or ch == BOT or ch == TOP
    
    def __isOperator(self, ch):
        return ch in CONNECTIVES or ch == NEG
  
    # Returns True if the precedence of operator is less than top of the stack, False otherwise
    def __not_greater(self, i): 
        try: 
            prec1 = self.precedence[i] 
            prec2 = self.precedence[self.__top()] 
            return prec1  < prec2
        except KeyError:  
            return False
              
    def infix_to_postfix_check(self, exp): 
        oprn_oprt = 0   # Grows with 1 when encountering an operand
                        # Decreases with 1 when encountering an operator
                        # String is not a WFF if the variable at any point goes below 0 or above 1

        negation = False # Gets set to True when encountering a negation
                         # String is not a WFF if a connective different from negation follows

        open_parentheses = 0    # Grows with 1 when encountering '('
                                # Decreases with 1 when encountering ')'
                                # String is not a WFF if the variable at any point goes below 0 or above 1
        
        last_connective = -1


        for count, c in enumerate(exp): 
            # Operand, add it to output 
            if self.__isOperand(c):
                last_connective = -1
                self.output.append(c)
                
                negation = False
                oprn_oprt += 1
                if oprn_oprt > 1:
                    print("String is not a WFF: expected connective at index " + str(count))
                    return False
              
            #'(', push it to stack
            elif c  == '(': 
                self.__push(c)
                negation = False

                open_parentheses += 1
  
            #')', pop and output from the stack until reaching '(' 
            elif c == ')':

                open_parentheses -= 1
                if open_parentheses < 0:
                    print("String is not a WFF: ')' closed but not opened at index " + str(count))
                    return False
                
                if not self.__isEmpty() and self.__top() == '(':
                    print("String is not a WFF: redundant parentheses closing at index " + str(count))
                    return False
                
                if oprn_oprt < 0 or negation == True:
                    print("String is not a WFF: expected WFF/Atom at index " + str(count))
                    return False

                while not self.__isEmpty() and self.__top() != '(': 
                    a = self.__pop() 
                    self.output.append(a) 

                if not self.__isEmpty() and self.__top() != '(': 
                    print("Error")
                    return False
                else: 
                    self.__pop() 
  
            # Operator
            elif self.__isOperator(c):
                last_connective = count
                if count == len(exp) - 1:
                    print("String is not a WFF: expected WFF/Atom at index " + str(count))
                    return False
                
                if c != NEG:

                    oprn_oprt -= 1
                    if oprn_oprt < 0 or negation == True:
                        print("String is not a WFF: expected WFF/Atom at index " + str(count))
                        return False
                else:
                    negation = True

                while not self.__isEmpty() and self.__not_greater(c): 
                    self.output.append(self.__pop()) 
                self.__push(c)
            else:
                print("String is not a WFF: illegal character at index " + str(count))
                return False
  
        # pop all the operators left from the stack 
        while not self.__isEmpty(): 
            self.output.append(self.__pop()) 
        
        if open_parentheses != 0:
            print("String is not a WFF: parentheses not closed properly!")
            return False

        if negation == True:
            print("String is not a WFF: no atom/WFF after negation!")
            return False
        
        if last_connective != -1:
            print("String is not a WFF: no atom/WFF for connective at index " + str(last_connective))
            return False
        
        return ("".join(self.output)) 
