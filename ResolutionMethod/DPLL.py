from DP import DavisPutnamTransformer
import copy

class DPLLTransformer(DavisPutnamTransformer):

    @classmethod
    def apply_DPLL(cls, clause_set):
        result, interpretation = cls.apply_DPLL_rec(clause_set, 1)
        return result

    @classmethod
    def apply_DPLL_rec(cls, clause_set, branch_id):
        interpretation = []
        modified = True
        while modified:
            interpretation_plr = cls.apply_pure_literal_rule(clause_set)
            interpretation += interpretation_plr

            interpretation_olr, is_unsatisfiable = cls.apply_one_literal_rule(clause_set)
            interpretation += interpretation_olr
            if is_unsatisfiable:
                return False, []
            
            # K' = {}, return True
            if len(clause_set.clauses) == 0:
                print("Reached empty clause set, therefore satisfiable for branch " + str(branch_id))
                return True, interpretation
            
            # Otherwise, split
            print("Splitting branch " + str(branch_id) + " into branches " + str(branch_id * 2) + " and " + str(branch_id * 2 + 1))

            # Determining the literal based on which to split 
            splitting_lit = max(clause_set.literal_count, key=lambda lit: clause_set.literal_count[lit] + clause_set.literal_count[-lit])
            if splitting_lit == None:
                break
            
            # Copying the set of clauses, and adding a clause to it containing just the literal
            branch_left = copy.deepcopy(clause_set)
            branch_left.add_clause([splitting_lit])

            left_truth_value, left_intr = cls.apply_DPLL_rec(branch_left, branch_id * 2)
            if left_truth_value == True:
                print("Left branch of branch " + str(branch_id) + " is satisfiable, we no longer check right branch")
                return True, interpretation + left_intr
            
            branch_right = copy.deepcopy(clause_set)
            branch_right.add_clause([-splitting_lit])

            right_truth_value, right_intr = cls.apply_DPLL_rec(branch_right, branch_id * 2 + 1)
            if right_truth_value == True:
                print("Right branch of branch " + str(branch_id) + " is satisfiable, therefore current branch also satisfiable")
                return True, interpretation + right_intr
            else:
                print("Branch " + str(branch_id) + " is unsatisfiable on both branches")
                return False, []
