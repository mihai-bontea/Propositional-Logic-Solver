# Propositional Logic Solver
testing

## The Resolution Method in Propositional Logic

### Problem statement:

Decide the satisfiability of a given formula given in "clause form".

### Theory basis:

K is a *propositional clause set* iff K is a finite set of propositional clauses.
C is a *propositional clause* iff C is a finite set of propositional literals.
L is a *propositional literal* is an atom, or the negation of an atom.

From any formula, we can obtain, in a natural way, its clause set form, by transforming it into CNF, and reading
the clauses directly from the disjuncts.

### Method of solving:

Resolution works by the following algorithm:

while exists C such that
    C is a propositional resolvent of two clauses in K' and C does not belong to K' already
do
    if C = {} then answer: "Not satisfiable"
    else K' := K' U {C}

answer: "Satisfiable"

