from Clause import Clause

class ClauseSet:
    def __init__(self):
        self.index = 1
        self.clauses = []
        self.literal_count = {}

    def add_clause(self, literals: set):
        # Updating the literal count
        for literal in literals:
            if literal in self.literal_count:
                self.literal_count[literal] += 1
            else:
                self.literal_count[literal] = 1
        
        # Creating a new clause out of the literals
        clause = Clause(literals, self.index)
        self.index += 1
        self.clauses.append(clause)
    
    def remove_clause(self, index: int):
        # Updating the literal count
        for literal in self.clauses[index].literals:
            self.literal_count[literal] -= 1
        
        self.clauses.pop(index)