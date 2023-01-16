# Assignment-2: Page Ranking of Web Graphs


## 2A
```
1. This assignment is aimed at implementing the PageRank algorithm from scratch.

2. The PageRank algorithm is implemented with and without random teleportations using the following two methods –
   
   A. Finding the principal left eigenvector of the probability transition matrix directly i.e., by making use of 
   numerical linear algebra packages
   B. Finding the principal left eigenvector of the probability transition matrix Power Iteration method.
```

The first two steps remain same for the both the parts

1. Construct Adjacency Matrix using `constructAdjM(input_file)`
2. Construct Probability transition Matrix `constructProbTransMatrix(V, adjM, random_teleport=True, alpha=0.9)` where alpha is the teleport operation probability
   
For part-1:
3. Compute principle left eigenvector via `compute_principle_left_eigen_vector(P)` which will be treated as steady state probabilities as well as ranks 

For part-2:
3. Use power iteration method until the vector converges. `power_iteration`. The converged vector is treated as steady-state vector.

4. To get the Pages in ranked order, use `get_ranks(pi)` where you feed in the steady state probabilities.

## 2B

```
1. This assignment is aimed at implementing the HITS algorithm from scratch.

2. The HITS implementation expects the near-steady state values of the Hub & Authority scores of the nodes
   in the given web graph.
   
3. The following functionality is required to be implemented:
   - Get the Hub & Authority Scores of each node in the base set for a particular query.
```

1. We use `construct_adjM(query, web_graph)` function to construct the adjacency matrix for the subgraph generated due to query 

2. We use fast method to compute the hub and authority score by computing principle eigenvector of A A.T and A.T A respectively
   
3. We rank the pages via hub and authority scores
