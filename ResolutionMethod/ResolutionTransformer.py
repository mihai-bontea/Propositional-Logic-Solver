from .ResolutionResultInfo import *
from .Clause import Clause

class ResolutionTransformer:
    @classmethod
    def get_clause_pairs(cls, clauses):
        for i in range(0, len(clauses) - 1):
            for j in range(i + 1, len(clauses)):
                yield (i, j)
    
    @classmethod
    def get_new_literals(cls, clauses, pair, literal):
        new_literals = clauses[pair[0]].literals | clauses[pair[1]].literals
        new_literals.discard(literal)
        new_literals.discard(-literal)
        return new_literals
    
    @classmethod
    def literal_and_complement_appears(cls, literal_count, literal):
        return -literal in literal_count.keys() and literal_count[literal] != 0 and literal_count[-literal] != 0
    
    @classmethod
    def is_clause_tautology(cls, literals):
        for literal in literals:
            if -literal in literals:
                return True
        return False
    
    @classmethod
    def apply_resolution(cls, clause_set):
        steps = []
        modified = True
        while modified == True:
            modified, is_not_satisfiable = cls.apply_resolution_once(clause_set, steps)
            if is_not_satisfiable:
                return ResolutionResultInfo(False, steps)
                    
        steps.append(("Nothing else to be done, therefore it is satisfiable.", LineEffect.GREEN))
        return ResolutionResultInfo(True, steps)
    
    @classmethod
    def apply_resolution_once(cls, clause_set, steps):
        modified = False
        for literal in clause_set.literal_count.keys():
                if cls.literal_and_complement_appears(clause_set.literal_count, literal):
                    for pair in cls.get_clause_pairs(clause_set.clauses):
                        if clause_set.clauses[pair[0]].contains_literal(literal) and \
                            clause_set.clauses[pair[1]].contains_literal(-literal):
                            
                            new_literals = cls.get_new_literals(clause_set.clauses, pair, literal)
                            if new_literals not in clause_set.clauses:
                                if not cls.is_clause_tautology(new_literals): 
                                    new_clause = clause_set.add_clause(new_literals)
                                    modified = True
                                    
                                    description_str = "From ({})({}) we have {}"\
                                        .format(str(clause_set.clauses[pair[0]].index),
                                                str(clause_set.clauses[pair[1]].index),
                                                str(new_clause))
                                    
                                    steps.append((description_str, LineEffect.CYAN))

                                    # We obtained the empty clause!
                                    if len(new_literals) == 0:
                                        steps.append(("We obtained {}, therefore not satisfiable.", LineEffect.RED))
                                        return True, True
        return modified, False
