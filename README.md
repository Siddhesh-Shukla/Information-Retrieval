# Information Retrieval

This repository contains Assignments for Information Retrieval for SEM-2 AY-2022

## 1: Boolean Retrieval System

1. This assignment is aimed at designing and developing Boolean Information Retrieval System, i.e., to return those documents (specifically their names from corpus/dataset given: point 7 of General Instructions) which satisfy Boolean (AND, OR and NOT with their combinations).

2. The Boolean Information Retrieval System should include the following features / pre-processing steps:
    - Stopword Removal: Remove the common stop words from the corpus.
    - Stemming or Lemmatization: Employ either one of the techniques for normalisation.
    - Wildcard Query Handling: Any one of the techniques among Permuterm or K-Gram index should be used for wildcard query management.
    - Spelling Correction: Edit Distance Method should be employed to correct misspelled words.

3. Try to vectorise your code as much as possible to make your computations faster and more efficient. Do not hard code any parts of the implementation unless it is indispensable. 


## 2: Page Ranking of Web Graphs

#### 2A

1. This assignment is aimed at implementing the PageRank algorithm from scratch.

2. The PageRank algorithm is implemented with and without random teleportations using the following two methods –
   
   - Finding the principal left eigenvector of the probability transition matrix directly i.e., by making use of 
   numerical linear algebra packages
   - Finding the principal left eigenvector of the probability transition matrix Power Iteration method.

#### 2B

1. This assignment is aimed at implementing the HITS algorithm from scratch.

2. The HITS implementation expects the near-steady state values of the Hub & Authority scores of the nodes
   in the given web graph.
   
3. The following functionality is required to be implemented:
   - Get the Hub & Authority Scores of each node in the base set for a particular query.

### Tech Stack 
```
1. NLTK
2. NumPy
3. Pandas
4. Matplotlib
```
