import numpy as np
import random

from __init__ import structure
import pandas as pd
import app

def run(problem, params):

    # Problem information
    costfunc = problem.costfunc
    nvar = problem.nvar
    varmin = problem.varmin
    varmax = problem.varmax
    # Problem constraints
    con_flags = problem.cons_flag

    # Parameters
    maxit = params.maxit
    npop = params.npop
    beta = params.beta
    pc =params.pc
    nc = int(np.round(pc*npop/2)*2)
    gamma = params.gamma
    mu = params.mu
    sigma = params.sigma
    crosspro = params.crosspro

    # Empty Individual Template
    empty_individual = structure()
    empty_individual.position = None
    empty_individual.cost = None
    empty_individual.constraints = []
    # BestSolution Ever Found
    bestsol = empty_individual.deepcopy()
    bestsol.cost = np.inf

    # Initialize Population
    pop = empty_individual.repeat(npop)
    for i in range(0, npop):
        pop[i].position = np.random.uniform(varmin, varmax, nvar)
        for j in range(0, len(costfunc(pop[i].position))-1):
            pop[i].constraints.append(costfunc(pop[i].position)[j+1])
    # Check initial population for constraints violation - death penalty
    apply_constraints(varmin, varmax, nvar, pop, costfunc, npop, con_flags)

    for i in range(0, npop):
        # pop[i].position = np.random.uniform(varmin, varmax, nvar)
        pop[i].cost = costfunc(pop[i].position)[0]
        # pop[i].cost = pd.eval("costfunc")(*pop[i].position)
        if pop[i].cost < bestsol.cost:
            bestsol = pop[i].deepcopy()

    # Best Cost of Iterations
    bestcost = np.empty(maxit)

    # Main Loop
    for it in range(maxit):


        popc = []
        for pop_it in range(nc//2):

            p1, p2 = tournament_selection(pop)


            # Perform Crossover
            r = np.random.rand()
            if r < crosspro:
                c1, c2 = singlepoint_crossover(p1, p2)
            else:
                c1, c2 = p1, p2

            # Perform Mutation
            c1 = mutate(c1, mu, sigma)
            c2 = mutate(c2, mu, sigma)
            children = [c1, c2]

            # Apply Constraints
            children = apply_constraints(varmin, varmax, nvar, children, costfunc, 2, con_flags)
            # Apply Bounds
            apply_bound(children[0], varmin, varmax)
            apply_bound(children[1], varmin, varmax)



            # Evaluate First Offspring
            children[0].cost = costfunc(children[0].position)[0]
            if children[0].cost < bestsol.cost:
                bestsol = children[0].deepcopy()

            # Evaluate Second Offspring
            children[1].cost = costfunc(children[1].position)[0]
            if children[1].cost < bestsol.cost:
                bestsol = children[1].deepcopy()

            # Add Offspring to popc
            popc.append(children[0])
            popc.append(children[1])

            # Merge, Sort and Select
            pop += popc
            pop = sorted(pop, key=lambda x: x.cost)
            pop = pop[0:npop]

            # Store Best Cost
            bestcost[it] = bestsol.cost

            # Show Iteration Information
            print("Iteration {}: Best Cost = {}:".format(it, bestcost[it]))
            # if pop_it == (nc // 2)-1:
            #     app.plot_graph(problem, pop, it, bestcost[it])
            #     print(bestcost[it])

    if nvar<=2:
        app.plot_graph(problem, pop, it, bestcost[it]) # wydrukuj jeden raz


    # Output
    out = structure()
    out.pop = pop
    out.bestsol = bestsol
    out.bestcost = bestcost
    return out

def crossover(p1, p2, gamma):
    c1 = p1.deepcopy()
    c2 = p1.deepcopy()
    alpha = np.random.uniform(-gamma, 1+gamma, *c1.position.shape)
    c1.position = alpha*p1.position + (1-alpha)*p2.position
    c2.position = alpha*p2.position + (1-alpha)*p1.position
    return c1, c2

def singlepoint_crossover(p1, p2):
    c1 = p1.deepcopy()
    c2 = p1.deepcopy()
    point = random.randint(0,len(c1))
    c1.position = np.append(p1.position[:point], p2.position[point:])
    c2.position = np.append(p2.position[:point], p1.position[point:])
    return c1, c2


def mutate(x, mu, sigma):
    y = x.deepcopy()
    flag = np.random.rand(*x.position.shape) <= mu
    ind = np.argwhere(flag)
    res= sigma*np.random.randn(*ind.shape)
    y.position[ind] += sigma*np.random.randn(*ind.shape)
    return y

def apply_bound(x, varmin, varmax):
    x.position = np.maximum(x.position, varmin)
    x.position = np.minimum(x.position, varmax)

def roulette_wheel_selection(p):
    c = np.cumsum(p)
    r = sum(p)*np.random.rand()
    ind = np.argwhere(r <= c)
    return ind[0][0]

def tournament_selection(pop):
    # while
    parents = random.choices(pop, k=5)
    # end while
    parents = sorted(parents, key=lambda pop: pop.cost, reverse=False)
    return parents[0], parents[1]

def apply_constraints(varmin, varmax, nvar, pop, costfunc, npop, con_flags): #added cons_flags
    death_flag = True
    c_list = []
    tolerance = 0.001
    c_flags_iterator = 0
    for i in range(0, npop):
        for element in range(1, len(costfunc(pop[i].constraints))):
            pop[i].constraints[element-1] = costfunc(pop[i].position)[element]
    for i in range(0, len(pop)):
        while (True):
            pop[i].position = np.random.uniform(varmin, varmax, nvar)
            for j in range(0, len(pop[i].constraints)):
                pop[i].constraints[j] = costfunc(pop[i].position)[j+1]
            for constraint in pop[i].constraints:
                if(con_flags[c_flags_iterator]=='Row' and (constraint-tolerance) <= 0.000):
                    c_list.append(True)
                elif (con_flags[c_flags_iterator] == 'NRow' and constraint < 0.000):
                    c_list.append(True)
                elif (con_flags[c_flags_iterator] == 'ORow' and constraint <= 0.000):
                    c_list.append(True)
                else:
                    c_list.append(False)
                if(constraint==pop[i].constraints[-1]):
                    c_flags_iterator=0
                else:
                    c_flags_iterator = c_flags_iterator + 1
            if(all(c_list)):
                c_flags_iterator=0
                break
            c_list = []

    return pop
