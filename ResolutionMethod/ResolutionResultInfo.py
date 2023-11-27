from enum import Enum

class LineEffect(Enum):
    GREEN = 1
    RED = 2
    CYAN = 3
    UNDERLINED = 4

class ResolutionResultInfo:
    def __init__(
        self,
        result: bool,
        steps: list,
        interpretation: list[int] = None
        ):
        self.result = result
        self.steps = steps
        self.interpretation = interpretation
