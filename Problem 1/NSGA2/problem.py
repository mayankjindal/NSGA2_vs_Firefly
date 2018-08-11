# Contains all information about the problem - the fitness functions, the
# bounds to the searchspace, etc

def fitness_1(x):
	return x[0]**2 - x[1]**2

def fitness_2(x):
	return x[0]**2 + x[1]**2

class Problem(object):
    # def __init__(self):
    lower_bound = [-2, -2]
    upper_bound = [2, 2]
    number_of_objectives = 2
    fitness_functions = [fitness_1,fitness_2]

# You want multiple objective functions for a single variable
# Eventually we need to add support to find the intersection of various
# search spaces


problem_instance = Problem()
