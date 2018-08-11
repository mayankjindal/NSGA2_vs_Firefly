# Handles all the code for each generation
import moga_constant as c
from genome import genome
import numpy.random as r
from problem import problem_instance as p
import random
import pprint


class generation(object):
    def __init__(self):
        # Stores all the members of the current generation Set
        self.population_members = []
        # self.fronts = []  # Stores all the fronts for each generation.
        self.matingpool = []  # Stores Mating Pool for the current Crossover
        self.no_of_fronts = 0  # Stores total Number of fronts.

    def initialize(self):
        self.population_members = [genome() for i in range(0, c.POPULATION_SIZE)]
        # print()
        # print(self.population_members)

    def merge(self, Qt):
        self.population_members += Qt
        self.count_number_of_fronts()

    def print_population(self):
        print('----Population Begin---------')
        from operator import methodcaller
        [x.print_genome() for x in self.population_members]
        print('----------Population End-----')

    def create_mating_pool(self, flag):
        # call flag as true if first iteration. else false
        # Run the tournament and return a matingpool
        # print("in create_mating_pool")
        if (flag):
            # print("in if")
            # if crowding distance isn't set use only front.
            while (len(self.matingpool) < len(self.population_members)):
                p = r.randint(0, len(self.population_members), 2)
                if (p[0] != p[1]):
                    geneA = self.population_members[p[0]]
                    geneB = self.population_members[p[1]]
                    if geneA.front < geneB.front:
                        self.matingpool.append(geneA)
                    elif geneA.front > geneB.front:
                        self.matingpool.append(geneB)
                    else:
                        self.matingpool.append(geneA)
                        self.matingpool.append(geneB)
                        # print("out if")
        else:
            # print("in else")
            while (len(self.matingpool) < len(self.population_members)):
                # print(self.population_members)
                # print(len(self.population_members))
                p = r.randint(0, len(self.population_members), 2)
                if (p[0] != p[1]):
                    geneA = self.population_members[p[0]]
                    geneB = self.population_members[p[1]]
                    if geneA.front < geneB.front:
                        self.matingpool.append(geneA)
                    elif geneA.front > geneB.front:
                        self.matingpool.append(geneB)
                    else:
                        if geneA.crowding_distance > geneB.crowding_distance:
                            self.matingpool.append(geneA)
                        elif geneA.crowding_distance < geneB.crowding_distance:
                            self.matingpool.append(geneB)
                        else:
                            self.matingpool.append(geneA)
                            self.matingpool.append(geneB)
                            # print("out else")
                            # print("out create_mating_pool")

    def perform_non_dominated_sort(self):
        for x in self.population_members:
            x.np = 0
        front_counter = 1
        temp_front = []
        next_front = []

        for a in self.population_members:
            for b in self.population_members:
                if (a != b):
                    if (a.dominates_lesser(b)):
                        a.Sp.add(b)
                    elif (b.dominates_lesser(a)):
                        a.np += 1
        from collections import defaultdict
        groups = defaultdict(list)
        for obj in self.population_members:
            groups[obj.np].append(obj)
        new_list = list(groups.values())
        temp_front = new_list[0]
        for x in temp_front:
            x.front = front_counter

        front_counter += 1
        while len(temp_front) > 0:
            list_of_sp = []
            list_of_np_zero = []
            for x in temp_front:
                for y in x.Sp:
                    list_of_sp.append(y)
            for x in list_of_sp:
                x.np -= 1
                if x.np == 0:
                    x.front = front_counter
                    list_of_np_zero.append(x)
            front_counter += 1
            temp_front = list_of_np_zero
        self.population_members.sort(key=lambda x: x.front)
        self.no_of_fronts = front_counter

    def calculate_crowding_distance(self):
        new_members = []
        # print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"+str(self.no_of_fronts)
        for front_no in range(1, self.no_of_fronts + 1):
            temp = [x for x in self.population_members if x.front == front_no]
            # for member in self.population_members:
            #     if member.front == front_no:
            #         temp.append(member)
            if (len(temp) == 1):
                temp[0].crowding_distance = float('inf')
            else:
                for member in temp:
                    member.crowding_distance = 0
                for y in range(0, p.number_of_objectives):
                    temp.sort(key=lambda x: x.objective_function_values[y])
                    temp[0].crowding_distance = float("inf")
                    temp[-1].crowding_distance = float("inf")
                    if temp[0].genes == temp[-1].genes:
                        for t in temp[1:-1]:
                            t.crowding_distance = 0
                            # for i in range(1, len(temp) - 1):
                            #     temp[i].crowding_distance = 0
                    else:
                        for i in range(1, len(temp) - 1):
                            temp[i].crowding_distance += (temp[i + 1].objective_function_values[y] -
                                                          temp[i - 1].objective_function_values[
                                                              y]) / (temp[len(temp) - 1].objective_function_values[y] -
                                                                     temp[0].objective_function_values[y])
            new_members += [x for x in temp]
            # for boob in temp:
            #     new_members.append(boob)
        self.population_members = []
        self.population_members += new_members

    def reproduce(self):
        offspring = []
        # print "mating pool"
        random.shuffle(self.matingpool)
        while (len(self.matingpool) > 1):
            parent1 = self.matingpool.pop()
            parent2 = self.matingpool.pop()
            child_tuple = self.simulated_binary_crossover(
                parent1.genes, parent2.genes)  # Genes instead of Gene
            offspring += [genome(x) for x in child_tuple]
            # for x in child_tuple:
            #     offspring.append(genome(x))
        # mutated_offspring = self.mutation_wraper(offspring)
        # return mutated_offspring
        return self.mutation_wraper(offspring)

    def simulated_binary_crossover(self, parent1, parent2):
        u = random.uniform(0, 1)
        if u <= 0.5:
            beta = (2 * u) ** (1 / (c.N + 1))
        else:
            beta = 1 / ((2 * (1 - u)) ** (1 / (c.N + 1)))

        def sbx(x, y, flag=False):
            if flag:
                return 0.5 * ((1 - beta) * x + (1 + beta) * y)
            else:
                return 0.5 * ((1 + beta) * x + (1 - beta) * y)

        child_1 = [sbx(x, y) for x, y in zip(parent1, parent2)]
        # for x,y in zip(parent1,parent2):
        #     child_1.append(0.5 * ((1 + beta) * x + (1 - beta) * y))
        child_2 = [sbx(x, y, True) for x, y in zip(parent1, parent2)]

        # for x,y in zip(parent1,parent2):
        #     child_2.append(0.5 * ((1 - beta) * x + (1 + beta) * y))
        # child_1 = 0.5 * ((1 + beta) * parent_1 + (1 - beta) * parent_2)
        # child_2 = 0.5 * ((1 - beta) * parent_1 + (1 + beta) * parent_2)
        return (child_1, child_2)

    def mutation_wraper(self, offspring):
        temp_list = []
        random.shuffle(offspring)
        for x in range(int(c.MUTATION_PROBABILITY * len(offspring))):
            # p = offspring.pop()
            temp_list.append(genome(self.polynomial_mutation(offspring.pop().genes)))
        offspring += temp_list
        # for x in temp_list:
        #     offspring.append(x)
        return offspring

    def count_number_of_fronts(self):
        frontset = set()
        for x in self.population_members:
            frontset.add(x.front)
        self.no_of_fronts = len(frontset)

    def polynomial_mutation(self, parent):
        u = random.uniform(0, 1)
        if u < 0.5:
            variation = ((2 * u) ** (1.0 / c.MUTATION_INDEX + 1)) - 1
        else:
            variation = 1 - ((2 * (1 - u)) ** (1.0 / c.MUTATION_INDEX + 1))

        for x, y, z in zip(parent, p.upper_bound, p.lower_bound):
            x = x + (y - z) * variation
        return parent

        # def nigger(self):
        #     for x in self.population_members:
        #         if(x.front == None):
        #             x.print_genome()

        # foo = generation()
        # foo.initialize()
        # foo.print_population()