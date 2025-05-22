# -*- coding: utf-8 -*-

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
        #Initial Population
        etapas_BWO = Etapas_BWO(self.nodos,self.n, self.k, self.d, self.cr, self.q, self.Q, self.c, self.mc, self.mx, self.dist, self.t, self.s, self.LS, self.LI,self.L, self.npop, self.nr, self.nm, self.ps)
        pop = etapas_BWO.inicializar_GA()
        inicio = time.time()
        pop = etapas_BWO.ordenar(pop)
        #Best solution
        gbest = pop[0]
        #Calculate Fitness Value
        fit_gbest = Fitness(gbest,self.dist,self.s,self.t, self.n, self.k, self.d, self.LS, self.LI).routeFitness()
        hist = []

        #BWO
        for i in range(0, self.max_iter):
            pop = etapas_BWO.ordenar(pop)

            #Best solution
            best = pop[0]
            fit_best = Fitness(best, self.dist,self.s,self.t, self.n, self.k, self.d, self.LS, self.LI).routeFitness()
            #Worst Solution
            worst = pop[self.npop-1]
            fit_worst = Fitness(worst, self.dist,self.s,self.t, self.n, self.k, self.d, self.LS, self.LI).routeFitness()
            #Update
            if fit_best < fit_gbest:
                gbest = best
                fit_gbest = Fitness(gbest, self.dist,self.s,self.t, self.n, self.k, self.d, self.LS, self.LI).routeFitness()
            hist.append(fit_gbest)
            final = time.time()
            iter_time = final - inicio
            
            inicio = time.time()
            
            # Procreation
            children = etapas_BWO.crossover(pop) 
            pop = pop + children
            
            # Mutation
            pop3 =  etapas_BWO.mutation(pop)
            pop = pop + pop3
            
            pop=etapas_BWO.ordenar(pop)
            
            # Best Population
            pop = pop[:self.npop]
        final2 = time.time()
        time_met = final2 - inicio1
        
        return fit_gbest, gbest, time_met, hist
