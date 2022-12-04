import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patheffects
from matplotlib import ticker
from __init__ import structure
from numpy import *
import matplotlib
import pandas as pd
from mpl_toolkits import mplot3d

class ReturnFunc:
    def __init__(self):
        self.obj = "-1"
        self.ci1 = "-1"
        self.ci2 = "-1"
        self.ci3 = "-1"
        self.ci4 = "-1"
        self.ci5 = "-1"
        self.nvar = "0"

    def func(self, x):

        obj = self.obj
        ci1 = self.ci1
        ci2 = self.ci2
        ci3 = self.ci3
        ci4 = self.ci4
        ci5 = self.ci5
        return [obj, ci1, ci2, ci3, ci4, ci5]


def func(x):
    obj = eval(funkcja_obj)
    ci1 = eval(funkcjaDlaApp.ci1)
    ci2 = eval(funkcjaDlaApp.ci2)
    ci3 = eval(funkcjaDlaApp.ci3)
    ci4 = eval(funkcjaDlaApp.ci4)
    ci5 = eval(funkcjaDlaApp.ci5)
    return [obj, ci1, ci2, ci3, ci4, ci5]

# Variables
funkcjaDlaApp = ReturnFunc()
funkcja_obj=-1
ogr_1=-1
ci1=-1
lista_ograniczen =[]


# Problem
problem = structure()
problem.costfunc = func
problem.nvar = int(funkcjaDlaApp.nvar)
problem.varmin = []
problem.varmax = []
problem.cons_flag=["NRow","NRow","NRow","NRow","NRow"]
problem.button_counter = 0
# GA params
paramsy = structure()
paramsy.maxit = 69
paramsy.npop = 20
paramsy.beta = 1
paramsy.pc = 1
paramsy.gamma = 0.1
paramsy.mu = 0.1
paramsy.sigma = 0.1
paramsy.crosspro = 0.8

def plot_graph(problem, pop, current_it, bestcost):

    matplotlib.use("Agg")
    tolerance = 0.001
    n_values = 100
    costfunc = problem.costfunc
    varmin_p = problem.varmin     #[startx, starty]
    varmax_p = problem.varmax     #[stopx, stopy]
    start_pos = [0] * problem.nvar
    stop_pos = [0] * problem.nvar
    X = [0] * problem.nvar
    pos_vals = [0] * problem.nvar
    for var_it in range(problem.nvar):
        start_pos[var_it], stop_pos[var_it] = varmin_p[var_it], varmax_p[var_it]
        pos_vals[var_it] = np.linspace(start_pos[var_it], stop_pos[var_it], n_values)

    if len(X) == 2:
        X[0], X[1] = np.meshgrid(pos_vals[0], pos_vals[1])
    elif len(X) == 3:
        X[0], X[1], X[2] = np.meshgrid(pos_vals[0], pos_vals[1], pos_vals[2])
    elif len(X) == 4:
        X[0], X[1], X[2], X[3] = np.meshgrid(pos_vals[0], pos_vals[1], pos_vals[2], pos_vals[3])
    elif len(X) == 5:
        X[0], X[1], X[2], X[3], X[4] = np.meshgrid(pos_vals[0], pos_vals[1], pos_vals[2], pos_vals[3], pos_vals[4])
    Z = problem.costfunc(X)[0]

    konsy=[0] * problem.button_counter
    for button_counter_plot in range(0, problem.button_counter):
        if button_counter_plot == 0:
            konsy[0]=problem.costfunc(X)[1]
            Z[konsy[0] >= 0] = nan
        if button_counter_plot == 1:
            konsy[1]=problem.costfunc(X)[2]
            Z[konsy[1] >= 0] = nan
        if button_counter_plot == 2:
            konsy[2]=problem.costfunc(X)[3]
            Z[konsy[2] >= 0] = nan
        if button_counter_plot == 3:
            konsy[3]=problem.costfunc(X)[4]
            Z[konsy[3] >= 0] = nan
        if button_counter_plot == 4:
            konsy[4]=problem.costfunc(X)[5]
            Z[konsy[4] >= 0] = nan

    # Axis
    fig = plt.figure(figsize=(6, 5))
    left, bottom, width, height = 0.1, 0.1, 0.8, 0.8
    ax = fig.add_axes([left, bottom, width, height])
    ax.set_title('Badany obszar')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    # Contours
    cp = plt.contourf(X[0], X[1], Z, 90, cmap='RdGy')
    for element in range(len(pop)):
        if pop[element].cost==bestcost:
            plt.scatter(pop[element].position[0], pop[element].position[1], c='teal', s=12)


    plt.colorbar(cp)

    # Saving graphs
    org_string = "Graphs/imageN.png"
    new_string = org_string.replace('N', str("0"))
    plt.savefig(new_string, bbox_inches='tight')
    print(new_string)
    plt.close('all')
