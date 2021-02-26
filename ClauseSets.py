from COLORS import style
import copy

class ClauseSet:

    def __init__(self):
        self.__index = 1
        self.__clauses = []
        self.__literal_count = {}

    def add_clause(self, literal_list):
        
        # Updating the literal count
        for literal in literal_list:
            if literal in self.__literal_count:
                self.__literal_count[literal] += 1
            else:
                self.__literal_count[literal] = 1
        
        # Creating a new clause out of the literals
        clause = Clause(literal_list, self.__index)
        self.__index += 1

        self.__clauses.append(clause)

    def apply_resolution(self):
        
        modified = True

        while modified == True:
            modified = False
            for literal in self.__literal_count.keys():
                if -literal in self.__literal_count.keys() and self.__literal_count[literal] != 0 and self.__literal_count[-literal] != 0:
                    for index_i in range(0, len(self.__clauses) - 1):
                        for index_j in range(index_i + 1, len(self.__clauses)):
                            if self.__clauses[index_i].contains_literal(literal) and self.__clauses[index_j].contains_literal(-literal):
                                new_literal_list = copy.deepcopy(self.__clauses[index_i].literals)
                                new_literal_list.remove(literal)

                                aux_literal_list = copy.deepcopy(self.__clauses[index_j].literals)
                                aux_literal_list.remove(-literal)

                                for lit in aux_literal_list:
                                    if lit not in new_literal_list:
                                        new_literal_list.append(lit)
                            
                                new_literal_list = sorted(new_literal_list)
                                clause = Clause(new_literal_list, self.__index)
                                if clause not in self.__clauses:
                                    self.add_clause(new_literal_list)

                                    modified = True
                                    print(style.GREEN("from (" + str(self.__clauses[index_i].index) + ')(' +  str(self.__clauses[index_j].index) + ')') + style.RESET(""), end=" ")
                                    print(style.CYAN("we have " + str(clause)) + style.RESET(""))

                                    # We obtained the empty clause!
                                    if len(clause) == 0:
                                        print(style.RED("We obtained {}, therefore Not Satisfiable") + style.RESET(""))
                                        return False
        
        print(style.GREEN("Nothing else to be done, therefore it is Satisfiable") + style.RESET(""))
        return True        
                    
    def apply_DP(self):
        
        modified = True

        while modified == True:
            modified = False

            """=================================================================="""
            to_delete = None
            # Finding a single literal for the 1-literal rule
            for clause in self.__clauses:
                if len(clause) == 1:
                    to_delete = clause.literals[0]
                    break
            
            # Applying the 1-literal rule if it is the case
            if to_delete != None:
                print(style.GREEN("Applying the 1-literal rule for the literal " + str(to_delete)) + style.RESET(""))
                modified = True
                # Removing clauses that contain the literal
                for i in range(len(self.__clauses) - 1, -1, -1):
                    # Found clause to delete
                    if self.__clauses[i].contains_literal(to_delete):
                        print(style.MAGENTA("Deleting the clause " + str(self.__clauses[i])) + style.RESET(""))
                        self.__remove_clause(i)
                
                # Removing the complement of the literals from clauses
                for i in range(len(self.__clauses) - 1, -1, -1):
                    # Remove the complement of the literal from the clauses that contain it
                    if self.__clauses[i].contains_literal(to_delete * -1):
                        self.__literal_count[to_delete * -1] -= 1
                        
                        print(style.MAGENTA("Removed literal " + str(to_delete * -1) + " from clause " + str(self.__clauses[i])) + style.RESET(""), end = "")
                        self.__clauses[i].remove_literal(to_delete * -1)
                        print(style.GREEN(", result: " + str(self.__clauses[i])) + style.RESET(""))
                        # We obtained the empty clause!
                        if len(self.__clauses[i]) == 0:
                            print(style.RED("We obtained {}, therefore Not Satisfiable") + style.RESET(""))
                            return False
            """=================================================================="""
            for literal in self.__literal_count.keys():
                if (literal * -1) not in self.__literal_count.keys() and self.__literal_count[literal] != 0:
                    # Applying the pure literal rule
                    modified = True
                    print(style.GREEN("Applying the pure literal rule for literal " + str(literal)) + style.RESET(""))
                    for i in range(len(self.__clauses) - 1, -1, -1):
                        # Found clause to delete
                        if self.__clauses[i].contains_literal(literal):
                            print(style.MAGENTA("Deleting the clause " + str(self.__clauses[i])) + style.RESET(""))
                            self.__remove_clause(i)
            """=================================================================="""
            for literal in self.__literal_count.keys():
                if -literal in self.__literal_count.keys() and self.__literal_count[literal] != 0 and self.__literal_count[-literal] != 0:
                    for index_i in range(0, len(self.__clauses) - 1):
                        for index_j in range(index_i + 1, len(self.__clauses)):
                            if self.__clauses[index_i].contains_literal(literal) and self.__clauses[index_j].contains_literal(-literal):
                                new_literal_list = copy.deepcopy(self.__clauses[index_i].literals)
                                new_literal_list.remove(literal)

                                aux_literal_list = copy.deepcopy(self.__clauses[index_j].literals)
                                aux_literal_list.remove(-literal)

                                for lit in aux_literal_list:
                                    if lit not in new_literal_list:
                                        new_literal_list.append(lit)
                            
                                new_literal_list = sorted(new_literal_list)
                                clause = Clause(new_literal_list, self.__index)
                                if clause not in self.__clauses:
                                    self.add_clause(new_literal_list)

                                    modified = True
                                    print(style.GREEN("from (" + str(self.__clauses[index_i].index) + ')(' +  str(self.__clauses[index_j].index) + ')') + style.RESET(""), end=" ")
                                    print(style.CYAN("we have " + str(clause)) + style.RESET(""))

                                    # We obtained the empty clause!
                                    if len(clause) == 0:
                                        print(style.RED("We obtained {}, therefore Not Satisfiable") + style.RESET(""))
                                        return False

        print(style.GREEN("Nothing else to be done, therefore it is Satisfiable") + style.RESET(""))
        return True 

    def __remove_clause(self, index):
        # Going over the literals in the clause to be deleted
        for literal in self.__clauses[index].literals:
            self.__literal_count[literal] -= 1
        
        # Pop it from the list
        self.__clauses.pop(index)

    def apply_DPLL(self, branch_id):

        interpretation = []    # 1

        print(style.UNDERLINE("On branch : " + str(branch_id)) + style.RESET(""))
        modified = True

        while modified == True:
            modified = False

            """=================================================================="""
            to_delete = None
            # Finding a single literal for the 1-literal rule
            for clause in self.__clauses:
                if len(clause) == 1:
                    to_delete = clause.literals[0]
                    break
            
            # Applying the 1-literal rule if it is the case
            if to_delete != None:

                interpretation.append(to_delete)        # 2

                print(style.GREEN("Applying the 1-literal rule for the literal " + str(to_delete)) + style.RESET(""))
                modified = True
                # Removing clauses that contain the literal
                for i in range(len(self.__clauses) - 1, -1, -1):
                    # Found clause to delete
                    if self.__clauses[i].contains_literal(to_delete):
                        print(style.MAGENTA("Deleting the clause " + str(self.__clauses[i])) + style.RESET(""))
                        self.__remove_clause(i)
                
                # Removing the complement of the literals from clauses
                for i in range(len(self.__clauses) - 1, -1, -1):
                    # Remove the complement of the literal from the clauses that contain it
                    if self.__clauses[i].contains_literal(to_delete * -1):
                        self.__literal_count[to_delete * -1] -= 1
                        
                        print(style.MAGENTA("Removed literal " + str(to_delete * -1) + " from clause " + str(self.__clauses[i])) + style.RESET(""), end = "")
                        self.__clauses[i].remove_literal(to_delete * -1)
                        print(style.GREEN(", result: " + str(self.__clauses[i])) + style.RESET(""))
                        # We obtained the empty clause!
                        if len(self.__clauses[i]) == 0:
                            print(style.RED("We obtained {}, therefore Not Satisfiable") + style.RESET(""))
                            return (False, [])
            """=================================================================="""
            for literal in self.__literal_count.keys():
                if (literal * -1) not in self.__literal_count.keys() and self.__literal_count[literal] != 0:
                    # Applying the pure literal rule

                    interpretation.append(literal)

                    modified = True
                    print(style.GREEN("Applying the pure literal rule for literal " + str(literal)) + style.RESET(""))
                    for i in range(len(self.__clauses) - 1, -1, -1):
                        # Found clause to delete
                        if self.__clauses[i].contains_literal(literal):
                            print(style.MAGENTA("Deleting the clause " + str(self.__clauses[i])) + style.RESET(""))
                            self.__remove_clause(i)
            """=================================================================="""
        
        # K' = {}, return True
        if len(self.__clauses) == 0:
            print(style.GREEN("Reached empty clause set, therefore satisfiable for branch " + str(branch_id)) + style.RESET(""))
            return (True, interpretation)
        # Otherwise, split
        print(style.MAGENTA("Splitting branch " + str(branch_id) + " into branches " + str(branch_id * 2) + " and " + str(branch_id * 2 + 1)) + style.RESET(""))

        max_count = 0
        splitting_lit = None
        # Choosing the literal to split on
        for literal in self.__literal_count:
            if literal >= 1:
                if (self.__literal_count[literal] + self.__literal_count[-literal]) > max_count:
                    max_count = (self.__literal_count[literal] + self.__literal_count[-literal])
                    splitting_lit = literal

        # Copying the set of clauses, and adding a clause to it containing just the literal
        branch_left = copy.deepcopy(self)
        branch_left.add_clause([splitting_lit])

        left_truth_value, intr_left = branch_left.apply_DPLL(branch_id * 2)
        if left_truth_value == True:
            print(style.GREEN("Left branch of branch " + str(branch_id) + " is satisfiable, we no longer check right branch") + style.RESET(""))
            return (True, interpretation + intr_left)
        
        branch_right = copy.deepcopy(self)
        branch_right.add_clause([splitting_lit * -1])

        right_truth_value, intr_right = branch_right.apply_DPLL(branch_id * 2 + 1)
        if right_truth_value == True:
            print(style.GREEN("Right branch of branch " + str(branch_id) + " is satisfiable, therefore current branch also satisfiable") + style.RESET(""))
            return (True, interpretation + intr_right)
        else:
            print(style.RED("Branch " + str(branch_id) + " unsatisfiable on both branches") + style.RESET(""))


class Clause:

    def __init__(self, literal_list, index):
        self.index = index
        self.literals = copy.deepcopy(literal_list)
        self.times_modified = 0

    def complemented(self):
        pass
    
    def copy(self):
        pass
    
    def contains_literal(self, literal):
        return literal in self.literals
    
    def remove_literal(self, literal):
        self.times_modified += 1
        self.literals.remove(literal)

    def __len__(self):
        return len(self.literals)
    
    def __eq__(self, rhs):
        return sorted(self.literals) == sorted(rhs.literals)

    def __str__(self):
        string = '(' + str(self.index) + ')'
        string += '{'
        if len(self) != 0:
            for i in range(0, len(self.literals) - 1):
                string += str(self.literals[i]) + ', '
            string += str(self.literals[-1])
        string += '}'

        return string