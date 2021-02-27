# Propositional Logic Solver
testing

## The Resolution Method in Propositional Logic

### Problem statement:

Decide the satisfiability of a formula given in "clause form". A formula is satisfiable if there exists some interpretation
for which the formula is evaluated to true.

### Theory basis:

* K is a *propositional clause set* iff K is a finite set of propositional clauses.
* C is a *propositional clause* iff C is a finite set of propositional literals.
* L is a *propositional literal* iff L is an atom, or the negation of an atom.

From any formula, we can obtain, in a natural way, its clause set form, by transforming it into CNF, and reading
the clauses directly from the disjuncts.

### Input format

The following three algorithms receive the input as 0-separated clauses, where each literal is an integer. The negative integers
represent the negation of an atom. As an example, the clause set **{{A ∨ B}, {A ∨ ¬C}}** would be represented as **1 2 0 1 -3**. This format is 
commonly used by SAT-solvers.

### Method of solving

The user can choose one of the following algorithms to determine the satisfiability of the formula. The input format is the same for all of them.
No steps are skipped, providing a verifiable output which resembles how one would solve the task on paper.

<details><summary>Propositional Resolution</summary>
<p>

#### Resolution uses the following algorithm:

```
K' := K
while exists C such that
    C is a propositional resolvent of two clauses in K' and C does not belong to K' already
do
    if C = {} then answer: "Not satisfiable"
    else K' := K' U {C}

answer: "Satisfiable"
```

</p>
</details>


<details><summary>Davis-Putnam(DP)</summary>
<p>
The Davis-Putnam method is an improvement to Propositional Resolution.
#### The following three steps are applied:

```
* the 1-literal rule
If a single literal L appears in a clause set, remove any instances of ¬L from the other clauses of K.

* the pure literal rule
If a literal occurs only positively or negatively in the clause set, delete all clauses containing it.

* resolution
Apply propositional resolution on the remaining clauses.

answer: "Satisfiable" when none of the rules can be applied
        "Not Satisfiable" when the empty clause is generated
```

</p>
</details>

