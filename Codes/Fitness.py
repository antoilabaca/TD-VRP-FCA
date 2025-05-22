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
            #print(self.route)
            d_values = [0] *(self.K)
            k=0
            for l in range(self.n + self.K+1, self.n + self.K+1 + self.D):
                d = self.route[l]
                #print(d)
                while d !=0:
                    d_values[k] = l-(self.n+self.K)
                    k = k+1
                    d=d-1
            #print(d_values)
            #si se tiene una nueva cadena se calcula el tiempo
            if self.Time_actual == 0:
                    
                for i in range(0,self.n+self.K): #se analiza primera parte de la cadena
                    fromClient = self.route[i] #se asigna i
                    toClient = self.route[i+1] #se asigna j
                    if fromClient == 0 and toClient != 0: #si i es cero, pero j es distinto de cero
                        #calculo tiempo desde depot a punto j
                        self.Time_actual =  self.LI[I] + round((self.dist[fromClient,toClient]/self.vel[fromClient,toClient,I]),3)
                        self.Arrive_Time[toClient] = self.Time_actual #guarda tiempo de llegada al nodo

                        #actualizar intervalo
                        while self.Time_actual > self.LI[I+1]:
                            I = I+1 
                        
                    if fromClient!=0 and toClient!=0: #si i y j son distintos de cero
                        #calculo tiempo desde punto i a punto j
                        #print("ti",tiempo_servicio)
                        try:
                            self.Time_actual = self.Time_actual + self.serviceTime[fromClient,d_values[V],I] + round((self.dist[fromClient,toClient]/self.vel[fromClient, toClient,I]),3)
                            self.Arrive_Time[toClient]= self.Time_actual #guarda tiempo de llegada al nodo
                        except:
                            self.Time_actual = 10
                            self.Arrive_Time[toClient] = 10
                        #actualizar intervalo
                        while self.Time_actual > self.LI[I+1]:
                            I = I+1
                   
                        
                    if fromClient !=0 and toClient == 0: #si j es cero, significa que termina el recorrido del vehículo
                        try:
                            self.Time_actual = self.Time_actual +  self.serviceTime[fromClient,d_values[V],I] + round((self.dist[fromClient,toClient]/self.vel[fromClient, toClient,I]),3)
                            self.Arrive_Time[toClient]= self.Time_actual #guarda tiempo de llegada al nodo
                        # Cuando encontramos un cero, agregamos el tiempo actual al vehículo actual
                        except:
                            self.Time_actual = 10
                            self.Arrive_Time[toClient] = 10
                        self.Time_por_vehiculo.append(self.Time_actual)
                        V = V+1 #pasa al siguiente vehículo
                        I = self.route[-1] 
                        #print(self.Time_por_vehiculo)
            fitness = max(self.Time_por_vehiculo) #guarda el fitness (valor F.O) como el tiempo max de los vehículos almacenados.
            return fitness

    def routeFitness(self):
            if self.fitness == 0:
                self.fitness = self.routeTime()
            return self.fitness