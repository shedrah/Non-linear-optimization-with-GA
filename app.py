import numpy as np
import matplotlib.pyplot as plt
from ypstruct import structure
import ga

#Funkcja testowa
def func(x):
    #return sum(x**2)
    return ((x[0]**2)+x[1]-11)**2+(x[0]+(x[1]**2)-7)**2

#Definicja problemu
problem = structure()
problem.costfunc = func
problem.nvar = 2
problem.varmin = -10
problem.varmax = 10

#Parametry GA
params = structure()
params.maxit = 100
params.npop = 20
params.beta = 1
params.pc = 1
params.gamma = 0.1
params.mu = 0.1
params.sigma = 0.1

#Algorytm genetyczny
out = ga.run(problem, params)

#Wynik
plt.plot(out.bestcost)
plt.xlim(0, params.maxit)
plt.xlabel('iterations')
plt.ylabel('best cost')
plt.title('GA')
plt.grid(True)
plt.show()