import csv
import numpy as np
from scipy.optimize import linprog, milp, LinearConstraint, Bounds



minimester_id = dict()

student_choices = []

with open('/Users/michaeliofin/Downloads/Topics Project/Topics-Project/choices.csv', mode ='r') as file:
  csvFile = csv.reader(file)
  next(csvFile)#skip a line

  #reading starting from second line
  for line in csvFile:
    ranking=[]
    for choice in line[1:]:
        if choice not in minimester_id:
            minimester_id[choice] = len(minimester_id)
        ranking.append(minimester_id[choice])
    student_choices.append(ranking)
        
#dictionary maps ids to names
minimester_dict = {v: k for k, v in minimester_id.items()}

num_students = len(student_choices)
num_minis=len(minimester_id)




cap = [num_students // num_minis*1.2] * num_minis
lcap = [num_students // num_minis*0.8] * num_minis

#add a clearing variable for each minimester
num_vars = num_students * num_minis + num_minis
c = np.zeros(num_vars)
happiness_array = [114, 113, 112, 109, 108, 107, 106, 104, 103, 102]
# happiness function
for i in range(num_students):
    for rank, j in enumerate(student_choices[i]):

        happiness = happiness_array[rank]
        idx = i * num_minis + j
        c[idx] = -happiness
#penalize deleting minimesters: "happiness for teachers"
for j in range(num_minis):
    c[num_minis*num_students+j]=200

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



A_ub = []
b_ub = []

for j in range(num_minis):
    row = np.zeros(num_vars)
    for i in range(num_students):
        row[i * num_minis + j] = 1
    row[num_minis*num_students+j] = cap[j]
    A_ub.append(row)
    b_ub.append(cap[j])
    A_ub.append(-row)
    b_ub.append(-lcap[j])

A_ub = np.array(A_ub)
b_ub = np.array(b_ub)


# Equality constraints  A_eq x = b_eq
eq_constraint = LinearConstraint(A_eq, b_eq, b_eq)

# Inequality constraints A_ub x <= b_ub
ub_constraint = LinearConstraint(A_ub, -np.inf, b_ub)

constraints = [eq_constraint, ub_constraint]

# Tell SciPy which variables are BINARY
integrality = np.ones(num_vars, dtype=int)


bounds = Bounds(0, 1)


res = milp(
    c=c,
    integrality=integrality,
    bounds=bounds,
    constraints=constraints
)



x = res.x[:-num_minis].reshape((num_students, num_minis))

assignments = {}
minimester_counts = {v: 0 for k, v in minimester_id.items()}
for i in range(num_students):
    j = int(np.argmax(x[i]))
    assignments[i] = j
    minimester_counts[j] += 1

choice_count={1: 0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0}

for i in range(num_students):
    print(student_choices[i])
    print(assignments[i])
    try:
        print(f"Student {i}: assigned to minimester '{minimester_dict[assignments[i]]}' (choice rank: {student_choices[i].index(assignments[i]) + 1})")
        choice_count[student_choices[i].index(assignments[i]) + 1]+=1
    except ValueError:
        print(f"Student {i}: assigned to minimester '{minimester_dict[assignments[i]]}' (choice rank: {11})")
        choice_count[11]+=1



print(minimester_counts)
print(minimester_dict[33])
print(choice_count)