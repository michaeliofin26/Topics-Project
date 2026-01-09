import random
import numpy as np
from scipy.optimize import linprog, milp, LinearConstraint, Bounds


#list of length 35, has each minimester probability

num_minis = 35
niners = 120
tenners = 122
eleveners = 116
twelvers = 128
num_students= niners + tenners + eleveners + twelvers
minimesters=list(range(num_minis))
minimester_popularities=[]
cap = [num_students // num_minis*3/2] * num_minis
lcap = [num_students // num_minis*1/2] * num_minis


sum = 0

for i in range(num_minis):
    n=random.random()
    minimester_popularities.append(n)
    sum+=n

for i in range(num_minis):
    minimester_popularities[i]/=sum

students = list(range(num_students))

student_choices = []

for i in students:
    new_choice = np.random.choice(minimesters,size=10,replace=False,p=minimester_popularities).tolist()
    student_choices.append(new_choice)

#add a clearing variable for each minimester
num_vars = num_students * num_minis + num_minis
c = np.zeros(num_vars)
happiness_array = [14, 13, 12, 9, 8, 7, 6, 4, 3, 2]
# happiness function
for i in range(num_students):
    for rank, j in enumerate(student_choices[i]):

        happiness = happiness_array[rank]
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
minimester_counts = {}
for i in range(num_students):
    j = int(np.argmax(x[i]))
    assignments[i] = j
    if j in minimester_counts:
        minimester_counts[j] += 1
    else:
        minimester_counts[j] = 1
     

minimester_dict = {
    0: "5 Museums In 4 Days",
    1: "Art World New York: Behind the Scenes",
    2: "Chinese Culture in NYC",
    3: "Queerfest NYC",
    4: "Rock The Apple In Español!",
    5: "Sweet History: Ice Cream and the Spice Trade",
    6: "The Godfather",
    7: "The Melting Pot EXPLORE MAGNIFY MAKE UNPLUG MOVE",
    8: "Intro. To Bouldering",
    9: "Outdoor Adventure and the Pursuit Of Happiness",
    10: "Art House Cinema",
    11: "The Beatles: Origin Story, Music, and More!",
    12: "Decoding Egyptian Hieroglyphs and Culture",
    13: "Food Justice NYC",
    14: "Immigration and Asylum-Seeking in New York City Today",
    15: "Latine Immigration & Culture: The American Dream Through Film & Food",
    16: "Learn to Fly!",
    17: "Mahjong 101",
    18: "Opera. That’s Right, Opera.",
    19: "Whodunit: A Mystery Minimester",
    20: "The Unseen Art World",
    21: "Cooking With Culture: A Hands On Cooking Class",
    22: "Escape Room Design",
    23: "Inside/Out: Sketching the City",
    24: "Knitting for Babies: Gifts of Warmth",
    25: "Learn How to Cook Chinese Food",
    26: "Let’s Bake!",
    27: "Lick Your Plate: Cooking Skills for Life",
    28: "Made In Brooklyn",
    29: "Weaving a Sustainable Future: Fiber Arts, Mending and Slow Fashion",
    30: "You Gotta Write for your Right...!",
    31: "Board Games",
    32: "Camp Crafts",
    33: "Challenging and Relaxing Discussion Sessions (C.A.R.D.S.)",
    34: "Notorious RPGS (Role-Playing Games)",
    35: "Soul & The City"
}

for i in range(len(students)):
    print(student_choices[i])
    print(assignments[i])
    print(f"Student {i}: assigned to minimester '{minimester_dict[assignments[i]]}' (choice rank: {student_choices[i].index(assignments[i]) + 1})")

print(minimester_counts)