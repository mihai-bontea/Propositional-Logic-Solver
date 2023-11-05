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
    def apply_resolution(cls, clause_set):
        modified = True
        while modified == True:
            modified = False
            for literal in clause_set.literal_count.keys():
                if cls.literal_and_complement_appears(clause_set.literal_count, literal):
                    for pair in cls.get_clause_pairs(clause_set.clauses):
                        if clause_set.clauses[pair[0]].contains_literal(literal) and \
                            clause_set.clauses[pair[1]].contains_literal(-literal):
                            
                            new_literals = cls.get_new_literals(clause_set.clauses, pair, literal)
                            if new_literals not in clause_set.clauses:
                                clause_set.add_clause(new_literals)

                                modified = True
                        
                                print("from ({})({}) we have {}"\
                                      .format(str(clause_set.clauses[pair[0]].index),
                                      str(clause_set.clauses[pair[1]].index), str(new_literals)))

                                # We obtained the empty clause!
                                if len(new_literals) == 0:
                                    print("We obtained {}, therefore Not Satisfiable")
                                    return False
        
        print("Nothing else to be done, therefore it is Satisfiable")
        return True