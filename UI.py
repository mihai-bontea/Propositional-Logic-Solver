from COLORS import style
from main import WFPropositionalFormula
from InfixToPostfix import Conversion
from ClauseSets import ClauseSet
import os, sys
import re

if sys.platform.lower() == "win32":
    os.system('color')

class UserInterface():

    def __init__(self):
        self.__filename = "example.txt"
        self.__options = {"1" : self.__truth_value_ui, "2" : self.__exp_tree, "3" : self.__proposition_type, "4" : self.__convert_to_NNF,
                          "5" : self.__convert_to_DNF, "6" : self.__convert_to_CNF, "7" : self.__resolution, "8" : self.__apply_DP,
                          "9" : self.__apply_DPLL}

    def __convert_str(self, user_input):
        """
        Replaces [1, 2, 3, 4, 5] with the respective connectives for the given string
        Removes whitespaces and newline characters that are left from reading from file
        Returns the list with the modifications
        """
        user_input = user_input.replace('!', '¬')
        user_input = user_input.replace('|', '∨')
        user_input = user_input.replace('&', '∧')
        user_input = user_input.replace('>', '→')
        user_input = user_input.replace('~', '↔')
        user_input = user_input.replace('1', '⊤')
        user_input = user_input.replace('0', '⊥')

        user_input = user_input.replace(' ', '')
        user_input = user_input.replace('\n', '')
        user_input = user_input.strip()

        return user_input

    def __truth_value_ui(self):
        """
        Reads a string from file. If it is a WFF it also reads an interpretation, and then
        computes the truth value of the proposition with respect to the given interpretation
        """
        try:
            with open(self.__filename, "r") as file:
                expr = file.readline()
                expr = self.__convert_str(expr)
                print(expr)

                form = WFPropositionalFormula(expr)
                if not form.is_WFF():
                    return

                form.store_as_exp_tree()

                second_line = file.readline()
                nr_atoms = int(second_line)
                value_dict = {}

                for i in range(nr_atoms):
                    line = file.readline()
                    line = line.split()

                    value = line[0]
                    truth_val = int(line[1])

                    if truth_val == 1:
                        value_dict[value] = True
                    else:
                        value_dict[value] = False

                form.compute_truth_value(value_dict)

        except IOError:
            pass
    
    def __proposition_type(self):
        """
        Reads a string from file. If it is a WFF, it tests whether it is a tautology, satisfiable,
        or inconsistent.
        """
        try:
            with open(self.__filename, "r") as file:
                expr = file.readline()
        
        except IOError:
            pass
        
        expr = self.__convert_str(expr)
        print(expr)

        form = WFPropositionalFormula(expr)
        if not form.is_WFF():
            return

        form.store_as_exp_tree()

        atoms = []

        for ch in expr:
            if ch.isalpha() == True and ch not in atoms:
                atoms.append(ch)
                
        form.proposition_type(atoms)
    
    def __exp_tree(self):
        """
        Prompts the user to enter a string representing a WFF, then stores the proposition as an
        expression tree
        """
        print(style.YELLOW("[ ¬ : 1 ][ ∨ : 2 ][ ∧ : 3 ][ → : 4 ][ ↔ : 5 ][ ⊤ : 6 ][ ⊥ : 7 ]") + style.RESET(""))
        expr = input(style.BLUE("Insert your expression(with the help of the table above: ") + style.RESET(""))
        expr = self.__convert_str(expr)
        print(expr)
        form = WFPropositionalFormula(expr)
        form.is_WFF()
        form.store_as_exp_tree()
        form.print_exp_tree()
    
    def __convert_to_NNF(self):
        print(style.YELLOW("[ ¬ : ! ][ ∨ : | ][ ∧ : & ][ → : > ][ ↔ : ~ ][ ⊤ : 1 ][ ⊥ : 0 ]") + style.RESET(""))
        expr = input(style.BLUE("Insert your expression(with the help of the table above: ") + style.RESET(""))
        expr = self.__convert_str(expr)
        print(expr)
        form = WFPropositionalFormula(expr)
        if form.is_WFF() == True:
            form.store_as_exp_tree()
            form.convert_to_NNF()
            form.print_exp_tree()
    
    def __convert_to_DNF(self):
        print(style.YELLOW("[ ¬ : ! ][ ∨ : | ][ ∧ : & ][ → : > ][ ↔ : ~ ][ ⊤ : 1 ][ ⊥ : 0 ]") + style.RESET(""))
        expr = input(style.BLUE("Insert your expression(with the help of the table above: ") + style.RESET(""))
        expr = self.__convert_str(expr)
        print(expr)
        form = WFPropositionalFormula(expr)
        if form.is_WFF() == True:
            form.store_as_exp_tree()
            form.convert_to_NNF()
            form.convert_to_DNF()

    def __convert_to_CNF(self):
        print(style.YELLOW("[ ¬ : ! ][ ∨ : | ][ ∧ : & ][ → : > ][ ↔ : ~ ][ ⊤ : 1 ][ ⊥ : 0 ]") + style.RESET(""))
        expr = input(style.BLUE("Insert your expression(with the help of the table above: ") + style.RESET(""))
        expr = self.__convert_str(expr)
        print(expr)
        form = WFPropositionalFormula(expr)
        if form.is_WFF() == True:
            form.store_as_exp_tree()
            form.convert_to_NNF()
            form.convert_to_CNF()

    def __resolution(self):
        expr = input(style.YELLOW("Enter the clauses: ") + style.RESET(""))
        clauses = expr.split("0")
        
        cs = ClauseSet()

        for clause in clauses:
            clause = clause.strip()

            print(clause)
            
            literal_list = []
            for num in clause.split(" "):
                literal_list.append(int(num))
            
            cs.add_clause(literal_list)

        cs.apply_resolution()
    
    def __apply_DP(self):
        expr = input(style.YELLOW("Enter the clauses: ") + style.RESET(""))
        clauses = expr.split("0")
        
        cs = ClauseSet()

        for clause in clauses:
            clause = clause.strip()

            print(clause)
            
            literal_list = []
            for num in clause.split(" "):
                literal_list.append(int(num))
            
            cs.add_clause(literal_list)

        cs.apply_DP()
    
    def __apply_DPLL(self):
        expr = input(style.YELLOW("Enter the clauses: ") + style.RESET(""))
        clauses = expr.split("0")
        
        cs = ClauseSet()

        for clause in clauses:
            clause = clause.strip()

            print(clause)
            
            literal_list = []
            for num in clause.split(" "):
                literal_list.append(int(num))
            
            cs.add_clause(literal_list)

        truth_val, intr = cs.apply_DPLL(1)

        if truth_val == True:
            print("A model for the formula given is: ", end = " ")
            print(intr)

    def __print_menu(self):
        print(style.BLUE("\n\nChoose one of the following options: ") + style.RESET(""))
        print(style.CYAN("1) Compute the truth value of the proposition from file") + style.RESET(""))
        print(style.CYAN("2) Store a formula as an expression tree, prints inorder traversal") + style.RESET(""))
        print(style.CYAN("3) Tells whether formula from file is valid/satisfiable/inconsistent(using backtracking)") + style.RESET(""))
        print(style.RED("<<Normal Form Transformations>>") + style.RESET(""))
        print(style.CYAN("4) Convert propositional formula to Negation Normal Form(NNF)") + style.RESET(""))
        print(style.CYAN("5) Convert propositional formula to Disjunctive Normal Form(DNF)") + style.RESET(""))
        print(style.CYAN("6) Convert propositional formula to Conjuctive Normal Form(CNF)") + style.RESET(""))
        print(style.RED("<<Propositional Resolution>>") + style.RESET(""))
        print(style.CYAN("7) Apply the resolution method on the clauses") + style.RESET(""))
        print(style.CYAN("8) Apply Davis-Putnam method(DP) on the clauses") + style.RESET(""))
        print(style.CYAN("9) Apply Davis-Putnam Logemann Loveland(DPLL) on the clauses") + style.RESET(""))
        print(style.RED("Or insert 'exit' to quit") + style.RESET(""))

    def start(self):

        while True:
            self.__print_menu()

            # Get user input    
            cmd = input((style.GREEN(">>> ") + style.RESET(" ")))
            
            if cmd == "exit":
                return 

            elif cmd in self.__options:
                self.__options[cmd]()
            

ui = UserInterface()
ui.start()