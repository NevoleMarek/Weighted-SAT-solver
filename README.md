# Variable weighted SAT Solver

This SAT Solver was created as a part of my final exam for subject NI-KOP at Faculty of Information Technology, Czech Technical University in Prague.

Benchmark report link: TBA

## Problem description

Given boolean formula $F$ of $n$ variables $X = (x_1,...,x_n)$ , vector of weights $W = (w_1,...,w_n)$. Find an assignment $Y = (y_1,...,y_n)$ that satisfies formula $F$ ($F(Y)=1$) and maximizes weight function c.
$$
c(Y,W) =\sum_{i=1}^n y_i w_i
$$

## Solver description

Solver implements 2 algorithms. Backtracking extended for Branch and Bound technique that prunes the search spaces using the weight function and metaheuristic of Simulated Annealing. Branch and Bound algorithm was used solely to get optimal solutions of test instances since it is a complete algorithm. Main focus was on variations heuristics and tuning of hyper parameters of the metaheuristic.

## Test instances description

[Test instances](test/) are for the most part in DIMACS CNF [format](https://people.sc.fsu.edu/~jburkardt/data/cnf/cnf.html). The only difference is the addition of variable weights line. This line starts with letter `w` and ends with `0` (zero). All of weights are in one line.

## Usage

```python
from formula import Formula
from simulatedannealing import SA_WeightedSAT
from branchandbound import BranchAndBound

formula = Formula.from_file(file)
solverSA = SA_WeightedSAT(formula,...)
solverBNB = BranchAndBound(formula)

weight, assignment = solverSA.run()
weight, assignment = solverBNB.run()
```

## Todo

- [x] Problem description
- [x] Test instances description
- [x] Usage description
- [ ] Benchmark reports
