import numpy as np 

def constructAdjM(input_file):
    '''
    Constructs adjacency matrix 
    '''
    with open(input_file, "r") as inFile:
        S = inFile.readline().split()
        V, E = int(S[0]), int(S[1])

        adjM = []

        for i in range(V):
            adjM.append(V * [0])

        for _ in range(E):
            S = inFile.readline().split()
            u, v = int(S[0]) - 1, int(S[1]) - 1
            adjM[u][v] = 1

        inFile.close()
    
    return V, E, adjM 

def constructProbTransMatrix(V, adjM, random_teleport=True, alpha=0.9):
    '''
    Constructs probability transition matrix using adjacency matrix 
    '''
    P = []
    for _ in range(V):
        P.append(V * [0])
    
    if random_teleport: 
        for i in range(V):
            connections = sum(adjM[i][:])
            if (connections == 0):
                for j in range(V):
                    P[i][j] = 1 / float(V)
            else:
                for j in range(V):
                    if adjM[i][j] == 1:
                        P[i][j] = 1 / float(connections)    

        P = np.array(P) 
        P = (1 - alpha) * P
        P = P + (alpha / float(V))
    
    else:
        for i in range(V):
            connections = sum(adjM[i][:])
            for j in range(V):
                if adjM[i][j] == 1:
                    P[i][j] = 1 / float(connections)
        
        P = np.array(P)
        
    return P


def compute_principle_left_eigen_vector(P):
    '''
    Computes principle left eigen vector using np
    Takes P matrix as input
    '''
    eigVals, eigVecs = np.linalg.eig(P)
    
    pi = eigVecs[:, eigVals.argmax()] # Compute with eigenvalue = 1
    norm_pi = pi / pi.sum()
    return norm_pi 

def get_ranks(pi):
    """
        Prints pages in rank order
    """
    
    ranks = np.argsort(pi)

    for i in range(len(ranks)):
        print(f"Rank {i + 1}:= Page {ranks[len(ranks) - i - 1] + 1}")

def power_iteration(V, P, threshold=1e-9):
    """
        Computes steady state probability distribution with power iteration method
    """

    x = np.array([1.0] + (V - 1) * [0.0]).reshape(1, -1)  # (1, V)

    t = 1
    while True:
        x = np.dot(x, P)     # x(t)
        y = np.dot(x, P)     # x(t + 1)
        delta = y - x

        if delta.all() < threshold:
            break 
        
        t += 1
        
    return x, t 

