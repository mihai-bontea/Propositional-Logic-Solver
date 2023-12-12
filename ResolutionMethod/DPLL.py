from .DP import DavisPutnamTransformer
from .ResolutionResultInfo import *
import concurrent.futures
import copy

class DPLLTransformer(DavisPutnamTransformer):

    @classmethod
    def apply_DPLL(cls, clause_set):
        result = cls.apply_DPLL_rec(clause_set, 1)
        return result

    @classmethod
    def apply_DPLL_rec(cls, clause_set, branch_id):
        steps = []
        interpretation = []

        steps.append(("On branch {}:".format(str(branch_id)), LineEffect.UNDERLINED))

        modified = True
        while modified:
            modified = False
            modified_plr = cls.apply_pure_literal_rule(clause_set, steps, interpretation)

            modified_olr, is_unsatisfiable = cls.apply_one_literal_rule(clause_set, steps, interpretation)
            modified = modified_plr or modified_olr

            if is_unsatisfiable:
                return ResolutionResultInfo(False, steps)
            
        # K' = {}, return True
        if len(clause_set.clauses) == 0:
            description_str = "Reached empty clause set, therefore satisfiable for branch {}.".format(str(branch_id))
            steps.append((description_str, LineEffect.GREEN))

            return ResolutionResultInfo(True, steps, interpretation)
        
        # Otherwise, split
        description_str = "Splitting branch {} into branches {} and {}.".format(str(branch_id), 
                                                                                str(branch_id * 2), 
                                                                                str(branch_id * 2 + 1))
        steps.append((description_str, LineEffect.CYAN))

        # Determining the literal based on which to split 
        splitting_lit = max(clause_set.literal_count, key=lambda lit: clause_set.literal_count[lit] + clause_set.literal_count[-lit])

        branch_left = copy.deepcopy(clause_set)
        branch_left.add_clause([splitting_lit])

        branch_right = copy.deepcopy(clause_set)
        branch_right.add_clause([-splitting_lit])

        with concurrent.futures.ProcessPoolExecutor() as executor:
            left_branch_res_future = executor.submit(cls.apply_DPLL_rec, branch_left, branch_id * 2)
            right_branch_res_future = executor.submit(cls.apply_DPLL_rec, branch_right, branch_id * 2 + 1)

            left_branch_res = left_branch_res_future.result()
            steps += left_branch_res.steps
            if left_branch_res.result == True:
                description_str = "Left child of branch {} is satisfiable. We no longer check right branch.".format(str(branch_id))
                steps.append((description_str, LineEffect.GREEN))

                return ResolutionResultInfo(True, steps, interpretation + left_branch_res.interpretation)

            right_branch_res = right_branch_res_future.result()
            steps += right_branch_res.steps
            if right_branch_res.result == True:
                description_str = "Right child of branch {} is satisfiable, therefore current branch is also satisfiable.".format(str(branch_id))
                steps.append((description_str, LineEffect.GREEN))
                
                return ResolutionResultInfo(True, steps, interpretation + right_branch_res.interpretation)
            else:
                steps.append(("Branch {} is unsatisfiable on both child branches.".format(str(branch_id)), LineEffect.RED))

                return ResolutionResultInfo(False, steps)
