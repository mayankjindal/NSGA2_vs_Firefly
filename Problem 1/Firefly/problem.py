# Contains all information about the problem - the fitness functions, the
# bounds to the search space, etc


def brightness_1(x):
    return x[0]**2 + x[1]**2


def brightness_2(x):
    return x[0]**2 - x[1]**2


class Problem(object):
    l_bound = [-2, -2]
    u_bound = [2, 2]
    no_of_objectives = 2
    brightness_functions = [brightness_1, brightness_2]


prob_inst = Problem()
