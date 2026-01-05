import random
import numpy as np
from scipy.optimize import linprog


#list of length 35, has each minimester probability

num_students = 400
num_minis = 35

minimesters=list(range(num_minis))
minimester_popularities=[]
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

