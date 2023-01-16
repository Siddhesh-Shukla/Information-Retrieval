import networkx as nx
import numpy as np 

def get_successors(i, web_graph):
    """
        Outputs successors of a node [List of nodes with outgoing edges to this node]
    """

    succ_edges = list(filter(lambda x: x[0] == i, web_graph.edges))
    successors = [i[1] for i in succ_edges]
    return successors

def get_predecessors(i, web_graph):
    """
        Outputs predecessors of a node [List of nodes with incoming edges to this node]
    """

    pred_edges = list(filter(lambda x: x[1] == i, web_graph.edges))
    predecessors = [i[0] for i in pred_edges]
    return predecessors

def construct_adjM(query, web_graph):
    """
        Constructs Adjacency matrix for the subsest of graph generated due to the query 
    """


    keywords = query.lower().split()
    keywords

    no_of_files = len(web_graph)
    nodes_satisfing_query = []

    for i in range(no_of_files):
        content = web_graph.nodes[i]['page_content'].lower()
        bool = True
        for word in keywords:
            if word not in content:
                bool = False
                break
        if bool:
            nodes_satisfing_query.append(i)


    nodes = set(nodes_satisfing_query)
    for node in nodes_satisfing_query:
        nodes.update(get_predecessors(node, web_graph))
        nodes.update(get_successors(node, web_graph))

    nodes = list(nodes)
    len(nodes)

    adj = []
    new = []
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if nodes[j] in get_successors(nodes[i], web_graph):
                new.append(1)
            else:
                new.append(0)
        adj.append(new)
        new = []

    A = np.array(adj)
    return A, nodes

