# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 12:08:28 2023

@author: user
"""

class Fitness:
    def __init__(self, route, dist, vel, serviceTime,n, K, D, LS,LI ):
        
        self.route = route
        self.fitness = 0.0
        self.Time_por_vehiculo = []
        self.Arrive_Time={}
        self.Time_actual = 0.0
        self.dist = dist
        self.vel = vel
        self.serviceTime = serviceTime
        self.n = n
        self.K = K
        self.D = D
        self.LS = LS
        self.LI = LI
        
    def routeTime(self):
            V = 0
            I = self.route[-1]
            d_values = [0] *(self.K)
            k=0
            for l in range(self.n + self.K+1, self.n + self.K+1 + self.D):
                d = self.route[l]
                while d !=0:
                    d_values[k] = l-(self.n+self.K)
                    k = k+1
                    d=d-1
                    
            if self.Time_actual == 0:
                    
                for i in range(0,self.n+self.K): 
                    fromClient = self.route[i] 
                    toClient = self.route[i+1] 
                    if fromClient == 0 and toClient != 0: #si i es cero, pero j es distinto de cero
                        self.Time_actual =  self.LI[I] + round((self.dist[fromClient,toClient]/self.vel[fromClient,toClient,I]),3)
                        self.Arrive_Time[toClient] = self.Time_actual #guarda tiempo de llegada al nodo

                        while self.Time_actual > self.LI[I+1]:
                            I = I+1 
                        
                    if fromClient!=0 and toClient!=0: #si i y j son distintos de cero
                            self.Time_actual = self.Time_actual + self.serviceTime[fromClient,d_values[V],I] + round((self.dist[fromClient,toClient]/self.vel[fromClient, toClient,I]),3)
                            self.Arrive_Time[toClient]= self.Time_actual 
                        while self.Time_actual > self.LI[I+1]:
                            I = I+1
                   
                        
                    if fromClient !=0 and toClient == 0: 
                            self.Time_actual = self.Time_actual +  self.serviceTime[fromClient,d_values[V],I] + round((self.dist[fromClient,toClient]/self.vel[fromClient, toClient,I]),3)
                            self.Arrive_Time[toClient]= self.Time_actual 
                        self.Time_por_vehiculo.append(self.Time_actual)
                        V = V+1 
                        I = self.route[-1] 
            fitness = max(self.Time_por_vehiculo) #guarda el fitness (valor F.O) como el tiempo max de los vehículos almacenados.
            return fitness

    def routeFitness(self):
            if self.fitness == 0:
                self.fitness = self.routeTime()
            return self.fitness
