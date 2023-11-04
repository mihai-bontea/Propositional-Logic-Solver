import copy

class Clause:

    def __init__(self, literal_set, index):
        self.index = index
        self.literals = copy.deepcopy(literal_set)
        self.times_modified = 0

    def contains_literal(self, literal):
        return literal in self.literals
    
    def remove_literal(self, literal):
        self.times_modified += 1
        self.literals.remove(literal)

    def __len__(self):
        return len(self.literals)
    
    def __eq__(self, rhs):
        return self.literals == rhs.literals

    def __str__(self): 
        comma_separated_str = ", ".join(str(num) for num in self.literals)      
        return "({} [{}])".format(str(self.index), comma_separated_str)
