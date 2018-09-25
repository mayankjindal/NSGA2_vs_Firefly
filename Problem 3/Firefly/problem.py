import constants as c
# Contains all information about the problem - the fitness functions, the
# bounds to the search space, etc


def brightness_1(x):
    return x[0]


def brightness_2(x):
    g = 1 + 9*(sum(x) - x[0])/(c.no_of_var - 1)
    f2 = g*(1 - (abs(x[0]/g))**0.5)

    return f2


class Problem(object):
    l_bound = [0]*30
    u_bound = [1]*30
    no_of_objectives = 2
    brightness_functions = [brightness_1, brightness_2]


prob_inst = Problem()
