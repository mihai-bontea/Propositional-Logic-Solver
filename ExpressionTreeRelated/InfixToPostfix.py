from Stack import Stack
from LogicOperators import *

class InfixToPostfixConverter:
    @staticmethod       
    def is_operand(char): 
        return (char.isalpha() and char.isupper()) or char == BOT or char == TOP
    
    @staticmethod
    def is_operator(char):
        return char in CONNECTIVES or char == NEG
  
    # Returns True if the precedence of operator is less than top of the stack, False otherwise
    @staticmethod
    def not_greater(operator, stack):
        try:
            precedence1 = OPERATOR_PRECEDENCE[operator]
            precedence2 = OPERATOR_PRECEDENCE[stack.top()] 
            return precedence1  < precedence2
        except KeyError:  
            return False
    
    @staticmethod
    def attempt_conversion(exp):
        stack = Stack()
        output = []

        oprn_oprt = 0   # Grows with 1 when encountering an operand
                        # Decreases with 1 when encountering an operator
                        # String is not a WFF if the variable at any point goes below 0 or above 1

        negation = False # Gets set to True when encountering a negation
                         # String is not a WFF if a connective different from negation follows

        open_parentheses = 0    # Grows with 1 when encountering '('
                                # Decreases with 1 when encountering ')'
                                # String is not a WFF if the variable at any point goes below 0
                                # Should be 0 at the end
        
        last_connective = -1    # Last index of a connective. Gets reset to -1 when encountering an operand
                                # Should be -1 at the end


        for count, char in enumerate(exp): 
            # Operand, add it to output 
            if InfixToPostfixConverter.is_operand(char):
                last_connective = -1
                output.append(char)
                
                negation = False
                oprn_oprt += 1
                if oprn_oprt > 1:
                    print("String is not a WFF: expected connective at index " + str(count))
                    return False
              
            #'(', push it to stack
            elif char  == '(': 
                stack.push(char)
                negation = False
                open_parentheses += 1
  
            #')', pop and output from the stack until reaching '(' 
            elif char == ')':

                open_parentheses -= 1
                if open_parentheses < 0:
                    print("String is not a WFF: ')' closed but not opened at index " + str(count))
                    return False
                
                if not stack.is_empty() and stack.top() == '(':
                    print("String is not a WFF: redundant parentheses closing at index " + str(count))
                    return False
                
                if oprn_oprt < 0 or negation == True:
                    print("String is not a WFF: expected WFF/Atom at index " + str(count))
                    return False

                while not stack.is_empty() and stack.top() != '(': 
                    a = stack.pop() 
                    output.append(a) 

                if not stack.is_empty() and stack.top() != '(': 
                    print("Error")
                    return False
                else: 
                    stack.pop() 
  
            # Operator
            elif InfixToPostfixConverter.is_operator(char):
                last_connective = count
                if count == len(exp) - 1:
                    print("String is not a WFF: expected WFF/Atom at index " + str(count))
                    return False
                
                if char != NEG:
                    oprn_oprt -= 1
                    if oprn_oprt < 0 or negation == True:
                        print("String is not a WFF: expected WFF/Atom at index " + str(count))
                        return False
                else:
                    negation = True

                while not stack.is_empty() and InfixToPostfixConverter.not_greater(char, stack): 
                    output.append(stack.pop()) 
                stack.push(char)
            else:
                print("String is not a WFF: illegal character at index " + str(count))
                return False
  
        # pop all the operators left from the stack 
        while not stack.is_empty(): 
            output.append(stack.pop()) 
        
        if open_parentheses != 0:
            print("String is not a WFF: parentheses not closed properly!")
            return False

        if negation == True:
            print("String is not a WFF: no atom/WFF after negation!")
            return False
        
        if last_connective != -1:
            print("String is not a WFF: no atom/WFF for connective at index " + str(last_connective))
            return False
        
        return ("".join(output))
    
print(InfixToPostfixConverter.attempt_conversion("(A→B)→C()"))