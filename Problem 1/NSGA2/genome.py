# Genome File
import moga_constant as c
from problem import problem_instance as p
from random import random
import pprint


class genome(object):
    def __init__(self, god=None):
        if god is None:
            # The actual Value of the gene
            self.genes = [random() * (2 ** (c.LENGTH_OF_BIT_STRING) - 1) for x in range(0, c.NUMBER_OF_VARIABLES)]
            # print("before scaling === "+str(self.genes[0]))
            self.genes = scale_genome(self.genes)
            # print("after scaling === "+str(self.genes[0]))
        else:
            self.genes = god
        self.front = None  # The front in which the genome lies. front = rank
        self.objective_function_values = [] # Stores the values of the gene along each objective function
        # Used for non dominated Sorting
        self.np = 0  # Domination Count according to NSGA
        self.Sp = set()  # Set of genomes dominated by the gene.
        # Used for Crowding distance
        self.crowding_distance = None
        self.evaluate_objective_functions()

    def print_genome(self):
        pprint.pprint('Gene: ' + repr(self.genes) \
                      + '\nfitnesses ' + repr(self.objective_function_values) \
                      + '\nnp: ' + repr(self.np) \
                      + '\nFront: ' + repr(self.front) \
                      + '\nCrowding Distance: ' + repr(self.crowding_distance))

    def evaluate_objective_functions(self):
        self.objective_function_values = [y(self.genes) for y in p.fitness_functions]
        # self.print_genome()

    def dominates_lesser(self, genome2):
        # TODO: CHECK RESPONSE FOR UNEQUAL LIST SIZES
        lesserorequal = 0
        for x, y in zip(self.objective_function_values, genome2.objective_function_values):
            if x <= y:
                lesserorequal += 1
        if (lesserorequal == p.number_of_objectives):
            return True
        else:
            return False

    def dominates_greater(self, genome_2):
        greaterorequal = 0
        for x, y in zip(self.objective_function_values, genome_2.objective_function_values):
            if x >= y:
                greaterorequal += 1
        if (greaterorequal == p.number_of_objectives):
            return True
        else:
            return False


def scale_genome(crud):
    # print("in scaling")
    # print(crud)
    temp = [(z + (y - z) * x / ((2 ** c.LENGTH_OF_BIT_STRING) - 1)) for x, y, z in
            zip(crud, p.upper_bound, p.lower_bound)]
    # for value in temp:
    # 	if value>2.0 or value <-2.0:
    # 		print("here")
    # print(temp)
    # for x,y,z in zip(crud,p.upper_bound,p.lower_bound):
    # 	print("x == "+str(x)+" y=="+str(y)+" z=="+str(z))
    # 	x=z+(y-z)*x/((2**c.LENGTH_OF_BIT_STRING)-1)
    # 	print("after x == " +str(x))
    return temp
    # return p.lower_bound + (p.upper_bound - p.lower_bound) * \
    #             crud / ((2**c.LENGTH_OF_BIT_STRING) - 1)