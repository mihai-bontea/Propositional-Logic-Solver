from abc import abstractmethod

class LawTransformerBase:
    """Base class for laws which transform an expression tree."""
    @staticmethod
    @abstractmethod
    def apply_law(expression_tree)->str:
        """ Should return the summary of the changes, or "" if it couldn't be applied.
            It shouldn't lead to any further changes when called again immediately after.
        """
        pass