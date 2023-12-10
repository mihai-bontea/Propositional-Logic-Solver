import sys
sys.path.append('.')
from ExpressionTreeRelated.InfixToPostfix import InfixToPostfixConverter
from ExpressionTreeRelated.ExpressionTree import ExpressionTree
from ResolutionMethod.ClauseSet import ClauseSet
from ResolutionMethod.ResolutionTransformer import ResolutionTransformer
from ResolutionMethod.DP import DavisPutnamTransformer
from ResolutionMethod.DPLL import DPLLTransformer
from enum import Enum

class ConversionType(Enum):
    NNF = 1
    CNF = 2
    DNF = 3


class ResolutionType(Enum):
    RES = 1
    DP = 2
    DPLL = 3


class Controller:
    def __init__(self) -> None:
        pass
    
    def convert_to_normal_forms(
        self,
        expr: str,
        conv_type: ConversionType
        ):
        try:
            # Turning the infix expression into postfix and constructing the expression tree based on it
            postfix = InfixToPostfixConverter.attempt_conversion(expr)
            expression_tree = ExpressionTree(postfix)
            
            # Executing the requested conversion type
            if conv_type == ConversionType.NNF:
                return expression_tree.convert_to_NNF()
            
            elif conv_type == ConversionType.CNF:
                return expression_tree.convert_to_CNF()
            
            return expression_tree.convert_to_DNF()

        except Exception as exc:
            return exc
    
    def is_proposition_satisfiable(
        self,
        clauses: str,
        res_type: ResolutionType
    ):
        try:
            clauses = clauses.split("0")
            clause_set = ClauseSet()
            
            # Constructing the clause set
            for clause in clauses:
                clause = clause.strip()
                if len(clause) > 0:
                    literal_list = [int(num) for num in clause.split(" ")]
                    clause_set.add_clause(set(literal_list))
            
            # Applying the requested resolution method
            if res_type == ResolutionType.RES:
                return ResolutionTransformer.apply_resolution(clause_set)
            
            elif res_type == ResolutionType.DP:
                return DavisPutnamTransformer.apply_DP(clause_set)
            
            return DPLLTransformer.apply_DPLL(clause_set)

        except Exception as exc:
            return exc