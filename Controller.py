import sys
sys.path.append('.')
from ExpressionTreeRelated.InfixToPostfix import InfixToPostfixConverter
from ExpressionTreeRelated.ExpressionTree import ExpressionTree
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
            postfix = InfixToPostfixConverter.attempt_conversion(expr)
            expression_tree = ExpressionTree(postfix)
            
            if conv_type == ConversionType.NNF:
                return expression_tree.convert_to_NNF()
            
            elif conv_type == ConversionType.CNF:
                return expression_tree.convert_to_CNF()
            
            return expression_tree.convert_to_DNF()

        except Exception as exc:
            return exc
    
    def is_proposition_satisfiable(
        self,
        clauses: list,
        res_type: ResolutionType
    ):
        pass
