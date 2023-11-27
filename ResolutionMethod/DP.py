from ResolutionTransformer import ResolutionTransformer

class DavisPutnamTransformer(ResolutionTransformer):
    @classmethod
    def apply_pure_literal_rule(cls, clause_set):
        interpretation = []
        repeat = True

        while repeat:
            repeat = False
            for literal in clause_set.literal_count.keys():
                if -literal not in clause_set.literal_count.keys() and clause_set.literal_count[literal] != 0:
                    interpretation.append(literal)
                    repeat = True
                    print("Applying the pure literal rule for literal " + str(literal))
                    for i in range(len(clause_set.clauses) - 1, -1, -1):
                        if clause_set.clauses[i].contains_literal(literal):
                            print("Deleting the clause " + str(clause_set.clauses[i]))
                            clause_set.remove_clause(i)

        return interpretation
    
    @classmethod
    def apply_one_literal_rule(cls, clause_set):
        interpretation = []
        while True:
            # Finding a literal that occurs only once in a clause
            literal_to_delete = next((list(clause.literals)[0] for clause in clause_set.clauses if len(clause) == 1), None)
            if literal_to_delete == None:
                break
            interpretation.append(literal_to_delete)
            
            
            # Deleting all clauses that contain the literal
            for i in range(len(clause_set.clauses) - 1, -1, -1):
                if clause_set.clauses[i].contains_literal(literal_to_delete):
                    print("Deleting the clause " + str(clause_set.clauses[i]))
                    clause_set.remove_clause(i)
            
            # Removing the literal's complement from the clauses
            for i in range(len(clause_set.clauses) - 1, -1, -1):
                if clause_set.clauses[i].contains_literal(-literal_to_delete):
                    print("Removing literal {} from clause {}".format(-literal_to_delete, str(clause_set.clauses[i])))
                    clause_set.clauses[i].remove_literal(-literal_to_delete)
                    clause_set.literal_count[-literal_to_delete] -= 1

                    # We obtained the empty clause!
                    if len(clause_set.clauses[i]) == 0:
                        print("We obtained {}, therefore Not Satisfiable")
                        return interpretation, True
        return interpretation, False

    @classmethod
    def apply_DP(cls, clause_set):
        modified = True
        while modified:
            modified_plr = len(cls.apply_pure_literal_rule(clause_set)) != 0
            
            interpretation_olr, is_unsatisfiable = cls.apply_one_literal_rule(clause_set)
            modified_olr = len(interpretation_olr) != 0
            if is_unsatisfiable:
                return False

            modified_res, is_unsatisfiable = cls.apply_resolution_once(clause_set)
            if is_unsatisfiable:
                return False

            modified = modified_plr or modified_olr or modified_res

        return True
