CONJ = '∧'
DISJ = '∨'
IMPL = '→'
EQUIV = '↔'
NEG = '¬'
TOP = '⊤'
BOT = '⊥'
CONNECTIVES = [EQUIV, IMPL, DISJ, CONJ]
OPERATOR_PRECEDENCE = {NEG : 5, DISJ : 4, CONJ : 3, IMPL : 2, EQUIV : 1}

OPERATOR_TO_FUNCT = {NEG : lambda truth_val : not truth_val,
                     EQUIV : lambda truth_val1, truth_val2 : truth_val1 == truth_val2,
                     IMPL : lambda truth_val1, truth_val2 : not (truth_val1 and not truth_val2),
                     DISJ : lambda truth_val1, truth_val2 : truth_val1 or truth_val2,
                     CONJ : lambda truth_val1, truth_val2 : truth_val1 and truth_val2}