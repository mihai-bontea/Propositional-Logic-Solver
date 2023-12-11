from .Clause import Clause
from .ResolutionTransformer import ResolutionTransformer

class ClauseSet:
    def __init__(self):
        self.index = 1
        self.clauses = []
        self.literal_count = {}

    def add_clause(self, literals: set):
        # Creating a new clause out of the literals
        clause = Clause(literals, self.index)

        if clause in self.clauses:
            return None

        # Updating the literal count
        for literal in literals:
            if literal in self.literal_count:
                self.literal_count[literal] += 1
            else:
                self.literal_count[literal] = 1
        
        self.index += 1
        self.clauses.append(clause)
        return clause
    
    def remove_clause(self, index: int):
        # Updating the literal count
        for literal in self.clauses[index].literals:
            self.literal_count[literal] -= 1
        
        self.clauses.pop(index)