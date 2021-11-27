# (Variable weighted SAT Solver

This SAT Solver was created as a part of my final exam for subject NI-KOP at Faculty of Information Technology, Czech Technical University in Prague.

Benchmark report link: TBA

## Problem description

Given boolean formula ![f](https://latex.codecogs.com/svg.latex?F) of ![n](https://latex.codecogs.com/svg.latex?n) variables ![X](https://latex.codecogs.com/svg.latex?X%20%3D%20%28x_1%2C...%2Cx_n%29), vector of weights ![W](https://latex.codecogs.com/svg.latex?W%20%3D%20%28w_1%2C...%2Cw_n%29). Find an assignment ![Y](https://latex.codecogs.com/svg.latex?Y%20%3D%20%28y_1%2C...%2Cy_n%29) that satisfies formula  ![F](https://latex.codecogs.com/svg.latex?F)(![FYeq1](https://latex.codecogs.com/svg.latex?F%28Y%29%3D1)) and maximizes weight function ![c](https://latex.codecogs.com/svg.latex?c)

<p align="center">
  <img width="460" height="300" src="https://latex.codecogs.com/svg.latex?c%28Y%2CW%29%20%3D%5Csum_%7Bi%3D1%7D%5En%20y_i%20w_i">
</p>

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
