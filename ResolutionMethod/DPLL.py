from DP import DavisPutnamTransformer

class DPLLTransformer(DavisPutnamTransformer):
    @classmethod
    def apply_DPLL(cls, clause_set, branch_id = 1):
        modified = True
        while modified:
            modified_plr = cls.apply_pure_literal_rule(clause_set)
            
            modified_olr, is_unsatisfiable = cls.apply_one_literal_rule(clause_set)
            if is_unsatisfiable:
                return False
            
            # K' = {}, return True
            if len(clause_set.clauses) == 0:
                print("Reached empty clause set, therefore satisfiable for branch " + str(branch_id))
                return (True, interpretation)
            # Otherwise, split
            print("Splitting branch " + str(branch_id) + " into branches " + str(branch_id * 2) + " and " + str(branch_id * 2 + 1))