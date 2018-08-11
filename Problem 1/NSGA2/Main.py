import time

t1 = time.time()   # Starting timestamp

import moga_constant as c
from Generation import generation
from genome import genome,scale_genome
import matplotlib.pyplot as plt
from problem import problem_instance as p

# from mpl_toolkits.mplot3d import Axes3D


p_0 = generation()
p_0.initialize()
x_fitness = []
y_fitness= []
# print 'PRE FIRST SORT'
# p_0.nigger()
# print("first population members")
# for foo in p_0.population_members:
# 	print(foo.genes);
p_0.perform_non_dominated_sort()
#p_0.population_members[0].print_genome()

q_0 = p_0.reproduce() # TODO:fix this shit
print("first kids == "+(str(len(q_0))))
combinePandQ = generation()
combinePandQ.merge(p_0.population_members)
combinePandQ.merge(q_0)
combinePandQ.perform_non_dominated_sort()
# print 'P AND Q MERGED AND SORTED'
# combinePandQ.print_population()
p_next = combinePandQ.population_members[:c.POPULATION_SIZE]

p_t = generation()
p_t.merge(p_next)
p_t.perform_non_dominated_sort()
p_t.count_number_of_fronts()
# print 'P1 SELECTED AND SORTED'
# p_t.print_population()
iteration_counter = 0
best_fit = []
while(iteration_counter<c.NUMBER_OF_ITERATIONS):
    best_fit.append(p_t.population_members[0].genes)
    print("iteration counter "+ str(iteration_counter))
    iteration_counter+=1
    # print "------------------iteration counter : " + repr(iteration_counter)
    # p_t.print_population()
    # p_t.print_population()
    # print("population members before crowding distance  === " + str(len(p_t.population_members)))
    # print(p_t.population_members)
    p_t.calculate_crowding_distance()
    #print iteration_counter
    # print("population members after crowding distance  === " + str(len(p_t.population_members)))
    # print(p_t.population_members)
    p_t.create_mating_pool(False)
    q_next = p_t.reproduce()
    q_next = [genome(scale_genome(x.genes)) for x in q_next]
    # for vale in q_next:
    # 	for val in vale:
    # 		if val>2 or val<-2:
    # 			print(val)
    # print("number of kids == "+(str(len(q_next))))
    combinePandQ = generation()
    combinePandQ.merge(p_t.population_members)
    combinePandQ.merge(q_next)
    combinePandQ.perform_non_dominated_sort()
    p_next = combinePandQ.population_members[:c.POPULATION_SIZE]
    p_t = generation()
    p_t.merge(p_next)
    p_t.perform_non_dominated_sort()
    p_t.count_number_of_fronts()
    # print p_t.population_members[-1].gene
    for member in p_t.population_members:
    	# print("members")
    	# print(member.genes)
    	x_fitness.append(p.fitness_functions[0](member.genes))
    	y_fitness.append(p.fitness_functions[1](member.genes))
# y = [x for x in range(0,c.NUMBER_OF_ITERATIONS)]
print(best_fit)


t2 = time.time()   # Final timestamp
print("Total Time = ", (t2 - t1))


# print(len(best_fit))
# print(len(y))
# plt.scatter(y, best_fit)
# plt.show()

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')


# xs = [x[0] for x in best_fit]
# ys = [y[1] for y in best_fit]
# zs = [x for x in range(0,c.NUMBER_OF_ITERATIONS)]
# print(xs)
# print(ys)
# ax.scatter(xs, ys, zs)

# ax.set_xlabel('X Label')
# ax.set_ylabel('Y Label')
# ax.set_zlabel('Z Label')
# # ax.set_ylim([-0.1,0.1])
# # ax.set_xlim([-0.1,0.1])
# plt.show()


# x_fitness.sort()
# y_fitness.sort()
# print x_fitness[-10:]
# print y_fitness[-10:]
# print(max(x_fitness))
# print(min(x_fitness))
# print(max(y_fitness))
# print(min(y_fitness))
plt.scatter(x_fitness,y_fitness)
plt.show()
# print x_fitness[-10:]
# print y_fitness[-10:]

# foo = generation()
# bitch1 = generation()
# foo.initialize()
# foo.perform_non_dominated_sort()
# for x in xrange(0,10):
#     bitch1 = generation()
#     bitch1.initialize()
#     foo.merge(bitch1.population_members)
#     foo.perform_non_dominated_sort()
#     foo.print_population()