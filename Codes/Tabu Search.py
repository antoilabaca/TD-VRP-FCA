# -*- coding: utf-8 -*-
"""
Created on Fri Aug 22 09:33:43 2025

@author: user
"""
from lector_matrices import LectorMatrices
from lector_test_instances import InstanceReader
from Fitness import Fitness
from calculos_BWO import Calculos_previos
import random
import time
from calculo_distancia import Calculo_Distancias

def InitialSolution(nodos, n, q, Q, d, k, cr, c, mc, mx):
    ruta = Calculos_previos(nodos,n, q, Q, d, k, cr, c, mc, mx).createRoute()
    #print(ruta)
    rutas_fact = Calculos_previos(nodos,n, q, Q, d, k, cr, c, mc, mx).FeasibilityRoute(ruta)
    #print(rutas_fact)
    crew = Calculos_previos(nodos,n, q, Q, d, k, cr, c, mc, mx).crewAssign()
    #print(crew)
   # l = random.randint(1,2)
    solution = rutas_fact + crew
    return solution    

def GenerateNeighborhood(sol,n, k, nodos,q, Q, d, cr, c, mc, mx):
    Neighborhood = []
    corte_cadena = n+k+1
    for i in range(corte_cadena):
        route = sol[:corte_cadena]
        assign = sol[corte_cadena:]
    
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
        
       
        routefact = Calculos_previos(nodos,n, q, Q, d, k, cr, c, mc, mx).FeasibilityRoute(route)

        if len(routefact) > corte_cadena:
            routefact = routefact[:corte_cadena]
        
        routefact = Calculos_previos(nodos,n, q, Q, d, k, cr, c, mc, mx).FeasibilityRoute(route)
        
        neighbor = routefact + assign
        Neighborhood.append(neighbor)
    return Neighborhood
        

    
def TS(max_iter, dist, s, t, n, k, d, LS, LI, nodos, q, Q, cr, c, mc, mx):
        sBest = InitialSolution(nodos, n, q, Q, d, k, cr, c, mc, mx)
        sCurrent = sBest
        tabuList = []
        fit_best = Fitness(sBest, dist, s,t, n, k, d, LS, LI).routeFitness()
        tabuList.append(sCurrent)
        inicio = time.time()
        for i in range(max_iter):
            print("i", i)
            sNeighbrhood = GenerateNeighborhood(sCurrent,n, k, nodos,q, Q, d, cr, c, mc, mx)
            print("genera vecindario")
            best_Candidate = 0
            fitBestCandidate = 100000000000
            for sCandidate in sNeighbrhood:
                if sCandidate not in tabuList:
                    fit = Fitness(sCandidate, dist, s,t, n, k, d, LS, LI).routeFitness()
                    if fit < fitBestCandidate:
                        best_Candidate = sCandidate
                        fitBestCandidate = fit
                        
            if best_Candidate == 0:
                break 
            else:
                sCurrent = best_Candidate
            
            if fitBestCandidate < fit_best:
                sBest = sCurrent                
                fit_best = Fitness(sCandidate,dist, s,t, n, k, d, LS, LI).routeFitness()
            tabuList.append(sCurrent)
        final = time.time()
        time_met = final - inicio
        return sBest, fit_best, time_met

def Instancia(archivo1, archivo2, archivo3, archivo4 ):
    data_reader = InstanceReader(archivo1)
    data_reader.read_instance()
    
    cat_reader = LectorMatrices(archivo3)
    cat_reader.leer_matriz() 

    t_dep = LectorMatrices(archivo2)
    t_dep.leer_matriz() 

    c_dcr = LectorMatrices(archivo4)
    c_dcr.leer_matriz()

    nodos = data_reader.get_column_values("CUSTNO")
    X = data_reader.get_column_values("XCOORD")
    Y = data_reader.get_column_values("YCOORD")
    tiempo_servicio = data_reader.get_column_values("SERVICETIME")
    
    
    n = len(nodos) #número de nodos
    k = 25 #número de vehículos
    d = 8 #cantidad de combinaciones de trabajadores
    l = 3 #numero de intervalos
    cr = 3 #numero de tipos de trabajadores 1[repartidores], 2[conductores], 3[multifuncionales]
    nodos.append(101)
    s = {}
    catheg = cat_reader.obtener_data()
    velocidades = t_dep.obtener_data()

    for i in nodos:
        for j in nodos:
            for t in range(0,l+100):
                try:
                    s[i,j,t] = velocidades[catheg[i,j],t]
                except:
                    s[i,j,t] = 0.3
    dist = {}
    for i in range(n):
        for j in range(n):
            x1 = X[i]
            y1 = Y[i]
            x2 = X[j]
            y2 = Y[j]
            dist[i,j] = Calculo_Distancias(x1, x2, y1, y2).distancia_euclidiana()
            dist[i,n] = 0
            dist[i,101] = 0
            dist[101,j] = 0
    t = {}        
    for i in range(n):
        for D in range(d+1):
            for L in range(l+100):
                try:
                    t[i,D,L] = tiempo_servicio[i]
                    t[100,D,L] = 0
                except: 
                    t[i,D,L] = 10

    c_ = c_dcr.obtener_data()

    c = {}

    for i in range(1,cr+1):
        for j in range(1,d+1):
            c[i,j] = c_[j,i]

    mx = {}
    for k in range(1,k+1):
        mx[k] = 5 #capacidad cabina vehiculo

    mc = {}
    mc[1] = 50
    for i in range(2,cr+1):
        mc[i] = 20 #cantidad de cada tipo de trabajadores disponibles

    q_i = data_reader.get_column_values("DEMAND")
    q={}
    for i in range(n):
        q[i]=q_i[i]
        q[n] = q_i[0]
        q[101] = 0

    LS={}
    LI ={}
    LI[1]=0 #Inicio de intervalos
    LI[0] = 0
    for i in range(2,l+100):
        LI[i] = LI[i-1]+ 480 #Definir tiempo entre intervalos
        LS[i-1]=LI[i]
    
    LS[l]=l*480 #tiempo entre intervalo

    inicio = 0
    #inicio = 1
    npop = 100
    pp = 0.6
    ps = 0.5
    pm = 0.1
    max_iter =100
    n=100
    print("termino carga")
    return nodos, n, k, d, l, cr, s, dist, t, c, mx, mc, q, LI, LS, npop, pp, ps, pm, max_iter
    

    
#Instancias
#archivos1
RC101 = "C:/Users/user/OneDrive - UNIVERSIDAD ANDRES BELLO/Documents/Doctorado/Investigación/Paper 1/Datos/git/RC101.txt"
RC201= "C:/Users/user/OneDrive - UNIVERSIDAD ANDRES BELLO/Documents/Doctorado/Investigación/Paper 1/Datos/git/RC201.txt"
C101 = "C:/Users/user/OneDrive - UNIVERSIDAD ANDRES BELLO/Documents/Doctorado/Investigación/Paper 1/Datos/git/C101.txt"
C201 = "C:/Users/user/OneDrive - UNIVERSIDAD ANDRES BELLO/Documents/Doctorado/Investigación/Paper 1/Datos/git/C201.txt"
R101 = "C:/Users/user/OneDrive - UNIVERSIDAD ANDRES BELLO/Documents/Doctorado/Investigación/Paper 1/Datos/git/R101.txt"
R201 = "C:/Users/user/OneDrive - UNIVERSIDAD ANDRES BELLO/Documents/Doctorado/Investigación/Paper 1/Datos/git/R201.txt"
    
archivos1 = [RC101, RC201, R101, R201, C101, C201, R101, R201]
    #ARCHIVOS2
t_dep = "C:/Users/user/OneDrive - UNIVERSIDAD ANDRES BELLO/Documents/Doctorado/Investigación/Paper 1/Datos/git/t_dep.txt"
t_dep_2 = "C:/Users/user/OneDrive - UNIVERSIDAD ANDRES BELLO/Documents/Doctorado/Investigación/Paper 1/Datos/git/t_dep_2.txt"
t_dep_3 = "C:/Users/user/OneDrive - UNIVERSIDAD ANDRES BELLO/Documents/Doctorado/Investigación/Paper 1/Datos/git/t_dep_3.txt"
    
archivos2 = [t_dep, t_dep_2, t_dep_3]
    #ARCHIVOS3
CAT1 = "C:/Users/user/OneDrive - UNIVERSIDAD ANDRES BELLO/Documents/Doctorado/Investigación/Paper 1/Datos/git/catheg.txt"
CAT2 = "C:/Users/user/OneDrive - UNIVERSIDAD ANDRES BELLO/Documents/Doctorado/Investigación/Paper 1/Datos/git/catheg_2.txt"
archivos3 = [CAT1, CAT2]
archivo4 = "C:/Users/user/OneDrive - UNIVERSIDAD ANDRES BELLO/Documents/Doctorado/Investigación/Paper 1/Datos/git/trabajadores.txt"
    
    #NP = [0.6]
    #CR = [0.5]
    #NM = [0.1]
    #NPOP = [20]
IMAX = 500
for i in range(9):
        #f = open("C:/Users/user/OneDrive - UNIVERSIDAD ANDRES BELLO/Documents/Doctorado/Investigación/Paper 1/Resultados/RESULTADOS TS Large Instance.txt","a")
        #f.write("\n Repetición %s" %(i))
        #f.close()
        for a1 in archivos1:
            for a2 in archivos2:
                for a3 in archivos3:
                        f = open("C:/Users/user/OneDrive - UNIVERSIDAD ANDRES BELLO/Documents/Doctorado/Investigación/Paper 1/Resultados/RESULTADOS TS Large Instance.txt","a")
                        f.write("\n SOLUCION INTANCIA %s - %s - %s" %(a1,a2,a3))
                        f.close()
                        nodos, n, k, d, l, cr, s, dist, t, c, mx, mc, q, LI, LS, npop, pp, ps, pm, max_iter = Instancia(a1, a2, a3, archivo4)
                        Q={}
                        if a1 == RC101:
                            for k in range(1,26):
                                Q[k] = 1000
                        if a1 == RC201:
                            for k in range(1,26):
                                Q[k] = 1000
                        if a1 == R201:
                            for k in range(1,26):
                                Q[k] = 1000
                        if a1 == C101:
                            for k in range(1,26):
                                Q[k] = 200
                        if a1 == R101:
                            for k in range(1,26):
                                Q[k] = 200
                        if a1 == C201:
                            for k in range(1,26):
                                Q[k] = 700
                        depot = 101
                        nodos_met = [valor for valor in nodos if valor != 0]
                        n_met = [valor for valor in nodos_met if valor != depot]
                        valor, solucion, tiempo = TS(IMAX, dist, s, t, n, k, d, LS, LI, n_met, q, Q, cr, c, mc, mx)
                        #solucion = VRPCFA(nodos, n, k, d, l, cr, s, dist, t, c, mx, mc, q, Q, LI, LS, depot = 101).VRPFCATime()
                        f = open("C:/Users/user/OneDrive - UNIVERSIDAD ANDRES BELLO/Documents/Doctorado/Investigación/Paper 1/Resultados/RESULTADOS TS Large Instance.txt","a")
                        f.write("\n 500 iteration")
                        f.write("\n Valor función objetivo: %s" %valor)
                        f.write("\n Solución:%s" %solucion)
                        f.write("\n Tiempo: %s" %tiempo)
                        #f.write("\n Historial: %s" %historial)
                        #f.write("\n Historial:%s" %historial)
                        f.close()
                
