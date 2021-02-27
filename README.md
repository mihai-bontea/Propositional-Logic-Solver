# Propositional Logic Solver

## Computing Truth Value

When selecting option 1(computing truth value), the program expects as input a line containing the proposition,
followed by n lines of atoms and their value. Based on this, a syntax tree is built, which is then used to compute
the truth value. Syntax errors are caught and pointed out in detail.

## Normal Forms

A formula F is in **negation normal form (NNF)**, iff:
* F is ⊤ or F is ⊥
* F is constructed from literals, using only the binary connectives '∧' and '∨'

A formula F is in **disjunctive normal form(DNF)**, iff F has the form F = F1 ∨ ... ∨ Fn, n ≥ 1, and
each of F1, ..., Fn is a conjunction of literals.

A formula F is in **conjunctive normal form(CNF)**, iff F has the form F = F1 ∧ ... ∧ Fn, n ≥ 1, and
each of F1, ..., Fn is a disjunction of literals.

### Transformation to NNF

The program is transforming the formula into NNF by applying the following formulae directly on the syntax tree representation 
of the given formula.

<details><summary>Formulae used in NNF conversion</summary>
<p>

* Reduction Laws:
```
(F ↔ G) ~ (F → G) ∧ (G → F)
(F → G) ~ (¬F ∨ G)
```

* Laws of "True" and "False":
```
¬⊤ ~ ⊥
¬⊥ ~ ⊤
F ∨ ⊥ ~ F
F ∧ ⊤ ~ F
F ∨ ⊤ ~ ⊤
F ∧ ⊥ ~ ⊥
⊥ → F ~ ⊤
F → ⊤ ~ ⊤
```

* Idempocy rules:
```
F ∧ F ~ F
F ∨ F ~ F
```

* Absorbtion Laws:
```
F ∨ (F ∧ G) ~ F
F ∧ (F ∨ G) ~ F
```

* "Annihilation" Laws:
```
F ∨ ¬F ~ ⊤
F ∧ ¬F ~ ⊥
F → F ~ ⊤
```

* Negation Laws:
```
¬(¬F) ~ F ("double negation")
¬(F ∨ G) ~ ¬F ∧ ¬G ("De Morgan")
¬(F ∧ G) ~ ¬F ∨ ¬G ("De Morgan")
```

</p>
</details>

### DNF Transformation

The program transforms the given propositional formula into an equivalent DNF by first transforming it into NNF, and then applying
the tautologies:

* F ∧ (G ∨ H) ~ (F ∧ G) ∨ (F ∧ H)
* (F ∨ G) ∧ H ~ (F ∧ H) ∨ (G ∧ H)

### CNF Transformation

Similarly, the formula is turned into NNF, and then the following tautologies are applied:

* F ∨ (G ∧ H) ~ (F ∨ G) ∧ (F ∨ H)
* (F ∧ G) ∨ H ~ (F ∨ H) ∧ (G ∨ H)

### Example

![cnf](https://user-images.githubusercontent.com/79721547/109398114-4efe7200-7943-11eb-8317-db279fe277e5.png)


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
No steps are skipped, providing a verifiable output which resembles how one would solve the task on paper. **Pseudocode and output examples available below.**

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

#### Output example:

![Res](https://user-images.githubusercontent.com/79721547/109392142-32ead880-7923-11eb-83f8-3377f00a47eb.png)

</p>
</details>


<details><summary>Davis-Putnam(DP)</summary>
<p>

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

#### Output example:

![DP](https://user-images.githubusercontent.com/79721547/109392082-d38cc880-7922-11eb-9952-653530650e87.png)

</p>
</details>


<details><summary>Davis-Putnam Logemann Loveland(DPLL)</summary>
<p>

#### The following three steps are applied:

```
* the 1-literal rule
If a single literal L appears in a clause set, remove any instances of ¬L from the other clauses of K.

* the pure literal rule
If a literal occurs only positively or negatively in the clause set, delete all clauses containing it.

* splitting
The satisfiability of K' is reduced to the satisfiability of K' ∪ {{L}}, K' ∪ {{¬L}}. 
(K' is satisfiable exactly if one of the two is).
```
#### Output example:

![DPLL](https://user-images.githubusercontent.com/79721547/109391999-5cefcb00-7922-11eb-96fd-0bcd9b204487.png)

</p>
</details>

## Acknowledgement
The theory is taken from DR. Adrian Craciun's lecture notes.

http://staff.fmi.uvt.ro/~adrian.craciun/lectures/logic/pdf/logicNotes.pdf