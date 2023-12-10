from .ResolutionTransformer import ResolutionTransformer
from .ResolutionResultInfo import *

class DavisPutnamTransformer(ResolutionTransformer):
    @classmethod
    def apply_pure_literal_rule(cls, clause_set, steps, interpretation):
        repeat = True
        modified = False

        while repeat:
            repeat = False
            for literal in clause_set.literal_count.keys():
                if -literal not in clause_set.literal_count.keys() and clause_set.literal_count[literal] != 0:
                    interpretation.append(literal)
                    modified = True
                    repeat = True

                    description_str = "Applying the pure literal rule for literal {}.".format(str(literal))
                    steps.append((description_str, LineEffect.CYAN))

                    for i in range(len(clause_set.clauses) - 1, -1, -1):
                        if clause_set.clauses[i].contains_literal(literal):

                            description_str = "Deleting the clause {}.".format(str(clause_set.clauses[i]))
                            steps.append((description_str, LineEffect.CYAN))

                            clause_set.remove_clause(i)

        return modified
    
    @classmethod
    def apply_one_literal_rule(cls, clause_set, steps, interpretation):
        modified = False
        while True:
            # Finding a literal that occurs only once in a clause
            literal_to_delete = next((list(clause.literals)[0] for clause in clause_set.clauses if len(clause) == 1), None)
            if literal_to_delete == None:
                break

            interpretation.append(literal_to_delete)
            modified = True
            
            # Deleting all clauses that contain the literal
            for i in range(len(clause_set.clauses) - 1, -1, -1):
                if clause_set.clauses[i].contains_literal(literal_to_delete):
                    description_str = "Deleting the clause {}.".format(str(clause_set.clauses[i]))
                    steps.append((description_str, LineEffect.CYAN))

                    clause_set.remove_clause(i)
            
            # Removing the literal's complement from the clauses
            for i in range(len(clause_set.clauses) - 1, -1, -1):
                if clause_set.clauses[i].contains_literal(-literal_to_delete):
                    description_str = "Removing literal {} from clause {}.".format(-literal_to_delete, str(clause_set.clauses[i]))
                    steps.append((description_str, LineEffect.CYAN))

                    clause_set.clauses[i].remove_literal(-literal_to_delete)
                    clause_set.literal_count[-literal_to_delete] -= 1

                    # We obtained the empty clause!
                    if len(clause_set.clauses[i]) == 0:
                        steps.append(("We obtained {}, therefore not satisfiable.", LineEffect.RED))
                        return True, True
        return modified, False

    @classmethod
    def apply_DP(cls, clause_set):
        steps = []
        modified = True
        while modified:
            modified_plr = cls.apply_pure_literal_rule(clause_set, steps, [])
            
            modified_olr, is_unsatisfiable = cls.apply_one_literal_rule(clause_set, steps, [])
            if is_unsatisfiable:
                return ResolutionResultInfo(False, steps)

            modified_res, is_unsatisfiable = cls.apply_resolution_once(clause_set, steps)
            if is_unsatisfiable:
                return ResolutionResultInfo(False, steps)

            modified = modified_plr or modified_olr or modified_res

        return ResolutionResultInfo(True, steps)
