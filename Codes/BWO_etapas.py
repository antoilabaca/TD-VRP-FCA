# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 22:15:57 2024

@author: antoi
"""
from calculos_BWO import Calculos_previos
from Fitness import Fitness

import operator
import random 
import numpy as np

class Etapas_BWO:
    def __init__(self,nodos, n,k,d,cr,q,Q,c,mc,mx,dist,t,s,LS,LI,L,npop, nr, nm, ps):
        self.nodos = nodos
        self.n = n
        self.k = k
        self.d = d
        self.cr = cr
        self.q = q
        self.Q = Q
        self.c = c
        self.npop = npop
        self.mc = mc
        self.mx = mx
        self.dist = dist
        self.s = s
        self.t = t
        self.LS = LS
        self.LI = LI
        self.L = L
        self.nr = nr
        self.nm = nm
        self.ps = ps
        self.clientList = Calculos_previos(self.nodos,self.n, self.q, self.Q, self.d, self.k, self.cr, self.c, self.mc, self.mx).ClientList()
        
    #iniciar población
    #Crear primera población (lista de rutas + asignación)
    ## inicializar población 
    def inicializar(self):
        population = []
        for i in range(0,self.npop):
            ruta = Calculos_previos(self.nodos,self.n, self.q, self.Q, self.d, self.k, self.cr, self.c, self.mc, self.mx).createRoute()
            rutas_fact = Calculos_previos(self.nodos,self.n, self.q, self.Q, self.d, self.k, self.cr, self.c, self.mc, self.mx).FeasibilityRoute(ruta)
            crew = Calculos_previos(self.nodos,self.n, self.q, self.Q, self.d, self.k, self.cr, self.c, self.mc, self.mx).crewAssign()
            l = random.randint(1,2)
            solution = rutas_fact + crew
            solution.append(l)
            population.append(solution)
        return population

    def rankRoutes(self,population):
        fitnessResults = {}
        for i in range(0,len(population)):
            fitnessResults[i] = Fitness(population[i],self.dist, self.s,self.t,self.n,self.k,self.d,self.LS,self.LI).routeFitness()
        sorted_results=sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = False)
        return sorted_results

    def ordenar(self, population):
        pop = []
        for i in range(len(population)) :
            index = self.rankRoutes(population)[i][0]
            pop.append(population[index])
        return pop

    def breed(self, parent1, parent2):
        child = []
        childP1 = []
        childP2 = []
        corte_cadena = self.n+self.k+1

        routep1 = parent1[:corte_cadena]
        routep2 = parent2[:corte_cadena]
        assign1 = parent1[corte_cadena:]
        assign2 = parent2[corte_cadena:]

        A = int(random.random() * len(routep1))
        B = int(random.random() * len(routep1))

        start = min(A, B)
        end = max(A, B)

        for i in range(start, end):
            childP1.append(routep1[i])

        childP2 =[item for item in routep2 if item == 0 or item not in childP1 ]

        child = childP1+childP2

        if child[0] !=0:
            child = [0] + child

            
        while len(child) > corte_cadena:
            found_zero = False # Variable de control para detectar el primer cero
            for i in range(1,len(child)):
                if child[i] == 0 and not found_zero:
                    del child[i]
                    found_zero = True  
                    break
                        
          
        if len(child) < corte_cadena:
            child = child.append(0)
            
        childfact = Calculos_previos(self.nodos,self.n, self.q, self.Q, self.d, self.k, self.cr, self.c, self.mc, self.mx).FeasibilityRoute(child)

        if len(childfact) > corte_cadena:
            childfact = childfact[:corte_cadena]
   
        
        child1 = childfact + assign1
        child2 = childfact + assign2
        
        
        #Father caniballism
        fitnessp1 = Fitness(parent1,self.dist,self.s, self.t,self.n, self.k, self.d, self.LS,self.LI).routeFitness()
        fitnessp2 = Fitness(parent2, self.dist, self.s, self.t, self.n, self.k, self.d, self.LS,self.LI).routeFitness()


        if fitnessp1 > fitnessp2:
            self.pop = np.delete(self.pop, parent2)
        else:
            self.pop = np.delete(self.pop, parent1)
            

        return child1, child2
    
    def crossover(self, pop): #nr población de reproductores
        children = []
        for i in range(0, self.nr-1):
            j = random.randint(0,self.npop-1)
            k = random.randint(0,self.npop-1)
            if j != k:
                ch1, ch2 = self.breed(pop[j], pop[k])
                children.append(ch1)
                children.append(ch2)
        children = self.ordenar(children)
        survive_children = int(round(self.nr*0.5))
        # children cannibalism (with mother)
        children = children[: survive_children]
      
        return children

    def mutation(self, pop):
        pop3 = []
        corte_cadena = self.n+self.k+1
        for i in range (0,self.nm):
            Mut = random.choice(pop)
            route = Mut[:corte_cadena]
            assign = Mut[corte_cadena:]
            
            m1 = random.choice(route[1:])
            m1 = route.index(m1)
            m2 = random.choice(route[1:])
            m2 = route.index(m2)
            route[m1], route[m2] = route[m2], route[m1]
            if route[0] !=0:
                route = [0] + route
                if len(route) > corte_cadena:
                    found_zero = False # Variable de control para detectar el primer cero
                    for i in range(1,len(route)):
                        if route[i] == 0 and not found_zero:
                            del route[i]
                            found_zero = True  # Establece la variable de control a True después de eliminar el cero
                            break
          
            if len(route) < corte_cadena:
                route = route.append(0)
                
               
            routefact = Calculos_previos(self.nodos,self.n, self.q, self.Q, self.d, self.k, self.cr, self.c, self.mc, self.mx).FeasibilityRoute(route)

            if len(routefact) > corte_cadena:
                routefact = routefact[:corte_cadena]

            M1 = routefact + assign
            pop3.append(M1)


        return pop3
