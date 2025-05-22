# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 21:24:46 2024

@author: antoi
"""
import random

class Calculos_previos:
    def __init__(self,nodos, n,q, Q, d, k, cr,c, mc, mx):       
        self.nodos = nodos
        self.n = n
        self.q = q
        self.Q = Q[1]
        self.d = d
        self.k = k
        self.cr = cr
        self.c = c
        self.mc = mc
        self.mx = mx
        self.clientList = self.ClientList()
       
        self.crew = []

        
    def ClientList(self):
        clientList = []
        for i in self.nodos:
            clientList.append(i)
        for k in range(self.k-1):
            clientList.append(0)
        
        return clientList
            
    def createRoute(self):
        route = []
        route = random.sample(self.clientList, len(self.clientList))
        route = [0] + route + [0]
        
        if route[0] !=0:
            route = [0] + route

        return route

    def calculoDemanda(self, route):
        #"capacidad": Calculo de capacidad
        demanda_por_vehiculo = []
        current_demand = 0
        for i in route:
            if i == 0:
                # Cuando encontramos un cero, agregamos la demanda actual al vehículo actual
                demanda_por_vehiculo.append(current_demand)
                current_demand = 0  # Reiniciamos la demanda actual
            else:
                # Sumamos la demanda del cliente actual a la demanda actual
                current_demand += self.q[i]
        return demanda_por_vehiculo

    def FeasibilityRoute (self, route):
        cd = self.calculoDemanda(route)
        factible = False
        while factible == False:
            if all(d <= self.Q for d in cd):
                factible = True
            else:
                del route
                route = self.createRoute()
                cd = self.calculoDemanda(route)
        
        return route
    
    # Asignación de equipos:
    def crewAssign(self): 
        #crea una lista de ceros
        cap_worker = {}
        cap_cabin ={}
        crew_fact = False
        cap_fact = False
        
        while crew_fact == False and cap_fact == False:
            #Elegir posición aleatoria para colocar 1
            self.crew = [0]*(self.d)
            #print(self.crew)
            for k in range(self.k):
                index = random.randint(0,self.d-1)
                #index = 4
                if self.crew[index] == 0:
                    self.crew[index] = 1
                else:
                    self.crew[index] = self.crew[index] + 1
            #print(self.crew)
            #evaluar factibilidad
            for cr in range(1,self.cr+1):
                cap_worker[cr] = sum(self.c[cr,d+1]*self.crew[d] for d in range(self.d))
            if all(cap_worker[cr]<=self.mc[cr] for cr in range(1,self.cr+1)):
                crew_fact = True
            else:
                cap_fact = False
            d_values = [0]*self.k
            k=0
            for l in range(self.d):
                d = self.crew[l]
                while d!=0:
                    d_values[k]=l+1
                    k = k+1
                    d = d-1
            for k in range(1,self.k+1):
                cap_cabin[k] = sum(self.c[self.cr, d_values[k-1]] for cr in range(1,self.cr+1))
            if all(cap_cabin[k] < self.mx[k] for k in range(1,self.k+1)):
                cap_fact = True
            else:
                crew_fact = False
        return self.crew
    
        
