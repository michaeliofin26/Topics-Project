import random
import numpy as np
from scipy.optimize import linprog


#list of length 35, has each minimester probability

num_students = 8
num_minis = 4

# minimesters=list(range(num_minis))
# minimester_popularities=[]
# sum = 0

# for i in range(num_minis):
#     n=random.random()
#     minimester_popularities.append(n)
#     sum+=n

# for i in range(num_minis):
#     minimester_popularities[i]/=sum

# students = list(range(num_students))

# student_choices = []

# for i in students:
#     new_choice = np.random.choice(minimesters,size=2,replace=False,p=minimester_popularities).tolist()
#     student_choices.append(new_choice)

student_choices =[[0, 3, 1, 2], [3, 1, 0, 2], [2, 3, 1, 0], [2, 0, 1, 3], [2, 3, 0, 1], [2, 1, 3, 0], [1, 2, 3, 0], [1, 3, 0, 2]]

num_vars = num_students * num_minis
c = np.zeros(num_vars)

for i in range(num_students):
    for rank, j in enumerate(student_choices[i]):
        happiness = 10 - rank
        idx = i * num_minis + j
        c[idx] = -happiness 

A_eq = []
b_eq = []

for i in range(num_students):
    row = np.zeros(num_vars)
    for j in range(num_minis):
        row[i * num_minis + j] = 1
    A_eq.append(row)
    b_eq.append(1)

A_eq = np.array(A_eq)
b_eq = np.array(b_eq)

cap = [2] * 4

A_ub = []
b_ub = []

for j in range(num_minis):
    row = np.zeros(num_vars)
    for i in range(num_students):
        row[i * num_minis + j] = 1
    A_ub.append(row)
    b_ub.append(cap[j])

A_ub = np.array(A_ub)
b_ub = np.array(b_ub)

bounds = [(0, 1)] * num_vars

res = linprog(
    c,
    A_eq=A_eq,
    b_eq=b_eq,
    A_ub=A_ub,
    b_ub=b_ub,
    bounds=bounds,
    method="highs"
)

x = res.x.reshape((num_students, num_minis))

assignments = {}

for i in range(num_students):
    j = int(np.argmax(x[i]))
    assignments[i] = j 

print(student_choices)
print(assignments)