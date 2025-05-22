# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 22:58:11 2024

@author: user
"""
from BWO_etapas import Etapas_BWO
from Fitness import Fitness

import time

class BWO:
    def __init__(self,nodos,n,k,d,cr,q,Q,c,npop,mc,mx,dist,s,t,LS,LI,L,pp,pm,ps,max_iter):
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
        self.pp = pp
        self.pm = pm
        self.ps = ps
        self.nr = int(self.npop*self.pp)
        self.nm = int(self.npop*self.pm)
        self.ns = int (self.npop*self.ps)
        self.max_iter = max_iter
    def bw_optimizer(self):
        inicio1 = time.time()
        # Inicializar población
        etapas_BWO = Etapas_BWO(self.nodos,self.n, self.k, self.d, self.cr, self.q, self.Q, self.c, self.mc, self.mx, self.dist, self.t, self.s, self.LS, self.LI,self.L, self.npop, self.nr, self.nm, self.ps)
        pop = etapas_BWO.inicializar_GA()
        inicio = time.time()

        # Evaluar población
        pop = etapas_BWO.ordenar(pop)
        #Elige el mejor
        gbest = pop[0]
        #Calcula fitness
        fit_gbest = Fitness(gbest,self.dist,self.s,self.t, self.n, self.k, self.d, self.LS, self.LI).routeFitness()
        hist = []

        # Iteraciones
        for i in range(0, self.max_iter):
          #  print("iteracion", i)
            pop = etapas_BWO.ordenar(pop)
            #pop2 = pop[:self.nr]       # poblacion resultante de la reproducción
            
            # Mejor solución
            best = pop[0]
            fit_best = Fitness(best, self.dist,self.s,self.t, self.n, self.k, self.d, self.LS, self.LI).routeFitness()
            #Peor solución
            worst = pop[self.npop-1]
            fit_worst = Fitness(worst, self.dist,self.s,self.t, self.n, self.k, self.d, self.LS, self.LI).routeFitness()
            #Actualización
            if fit_best < fit_gbest:
                gbest = best
                fit_gbest = Fitness(gbest, self.dist,self.s,self.t, self.n, self.k, self.d, self.LS, self.LI).routeFitness()
            hist.append(fit_gbest)
            final = time.time()
            iter_time = final - inicio

           # if i % 1 == 0:
            #    f = open("C:/Users/user/OneDrive - UNIVERSIDAD ANDRES BELLO/Documents/Doctorado/Investigación/Paper 1/Resultados/RESULTADOS BWO 2.txt","a")
             #   f.write("Iteración: %s    Mejor Resultado:%s  Peor Resultado:%s " %(i, fit_best, fit_worst))
              #  f.write("Tiempo de iteración:%s " %iter_time)
               # f.close()
            inicio = time.time()

            # Reproduciones
            children = etapas_BWO.crossover(pop) #tiene canibalismo padre e hijos
            #print("termina reproduccion")
            # ordenar por fitness (si no se realiza canibalismo)
            #children  = etapas_BWO.ordenar(children)
            pop = pop + children
            
            # Mutaciones
            pop3 =  etapas_BWO.mutation(pop)
            #print("termina mutacion")
            pop = pop + pop3
            # ordenar por fitness
            pop=etapas_BWO.ordenar(pop)
            # Selección de mejores resultados
            pop = pop[:self.npop]
        final2 = time.time()
        time_met = final2 - inicio1
        #print("Tiempo de ejecución: %s" %time_met)
       # f = open("C:/Users/user/OneDrive - UNIVERSIDAD ANDRES BELLO/Documents/Doctorado/Investigación/Paper 1/Resultados/RESULTADOS BWO 2.txt","a")
        #f.write("Tiempo de ejecución: %s" %time_met)
        #f.close()
        return fit_gbest, gbest, time_met, hist