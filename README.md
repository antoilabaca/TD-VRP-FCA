# TD-VRP-FCA
Repository data for TD-VRP-FCA
This repository shows the data is separated into 3 groups of instances to solve The Time-Dependent Vehicle Routing Problem with Fleet and Crew Assignment where a mathematical model is formulated and an algorithm based on Black Widow Optimizer (Hayyolalam and Kazem, 2020) with Fitness calculation is designed through a constructive heuristic as an alternative to the mathematical model. 
The necessary parameters for the model and the algorithm are the following:
- $I$ set of customers/buildings
- $o,s$ depot nodes 
- $N$   set of nodes: $N=I \cup \{o,s\}$  
- $A$ set of arcs: $A=\{(i,j): i,j \in N, i\neq j\}$ 
- $K$            set of vehicles  
- $D$            set of crew combination  
- $L$            set of time intervals  
- $C$            set of worker types 
- $v_{ij}^l$      speed for each time interval $l\in L$ between each pair of nodes $i\in N, j \in N \setminus \{i\}$  
- $\delta_{ij}$  distance between each pair of nodes: $i\in N, j \in N \setminus \{i\}$ 
- $t_{id}^l$      service time for each customer $i\in I$ served with crew combination $d\in D$ in the time interval $l\in L$  
- $\omega_{d}^c$     number of workers type $c \in C$ in each crew combination $d\in D$   
- $W^k$       maximum crew number for each vehicle $k \in K$   
- $V^c$      maximum number of workers $c\in C$ in a crew  
- $q_i$         demand for each node $i\in N: q_o=q_s=0$   
- $Q^k$         capacity for each vehicle $k\in K$ 
- $Ll^l$        lower limit time interval  $l \in L$   
- $Ul^l$        upper limit time interval $l\in L$ 
Los set de instancias se separan de la siguiente manera:
# Small Intance
Based on Allen et al. (2019) intance the following files are shown:
- C: shows information of the workers ($D$, $C$, $\omega_{d}^c$)
- coord: coordinates of each node
- Distances: distance between each point ($\omega_{d}^c$)
- t: service time for each customer served with crew combination in the time interval ($t_{id}^l$)
- K: vehicle data  ($K$, $Q^k$, $W^k$)
- v: speed for each time interval between each pair of nodes ($v_{ij}^l$)
# Large Intance
Based in Balseiro et al. (2011) with some of the files described at https://github.com/yma17/tdvrptw-snrpga2/tree/main/data/instances without modifications, only D file identical to small intance was added.
# Case Study
Data extracted from a delivery company, the folder contains the same files as Small Intance but for each of the 12 instances created.
