import numpy as np
# Contains all information about the problem - the fitness functions, the
# bounds to the search space, etc
'''
 net_x = 0
    for i in x:
        net_x += (i - (3**(-0.5)))**2
    return 1 - np.exp(-net_x)
'''


def brightness_1(x):
    return x[0]**2


def brightness_2(x):
    return (x[0] - 2)**2


class Problem(object):
    l_bound = [-2]
    u_bound = [2]
    no_of_objectives = 2
    brightness_functions = [brightness_1, brightness_2]


prob_inst = Problem()
