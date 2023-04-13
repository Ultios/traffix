import networkx as nx
import pandas as pd
import numpy as np

def line_search(row, a, alpha, beta):
    t=row['initial_travel_time']
    x=row['flow']
    y=row['auxflow']
    c=row['capacity']
    return -t*(x-y)*(alpha*(((x+a*(y-x))/c)**beta)+1)

def bisection(G, xl=0, xr=1, delta=0.0002, alpha=0.15, beta=4):
    n = 0
    df = nx.to_pandas_edgelist(G)
    condition = True
    while condition:
        n += 1
        x = (xl+xr)/2
        if df.apply(lambda row: line_search(row, x, alpha=alpha, beta=beta), axis = 1).sum() <= 0:
            xl = x
        else:
            xr = x
        condition = abs(xr-xl) > 2*delta
        # print('|xl-xr| =', abs(xr-xl),' xl =', xl, ' xr=',xr)
    #print(f"number of iteration in bisection method is {n} with alpha = {(xr+xl)/2}")
    return (xr+xl)/2

def update(row, alpha):
    return row['flow'] + alpha * (row['auxflow'] - row['flow'])

def update_mainflow(G, alpha):
    df = nx.to_pandas_edgelist(G, edge_key='ekey').set_index(["source","target","ekey"])
    df['flow'] = df.apply(lambda row: update(row, alpha), axis=1).values
    nx.set_edge_attributes(G, df['flow'], name='flow')
    return G  

def CCA(G, nodes_OD, flow, number_of_iteration=10000, alpha=0.15, beta=4):
    #Initialize initial time_travel column based on travel time column 
    #from ox.add_edge_travel_times
    G = add_edge_initial_travel_time(G)
    
    # Initialize flow from OD Matrices, do shortest path
    # and Assign flow to all links.
    G = OD_shortest_path(G, nodes, flow, flow_type='flow')
    
    condition = True
    n = 0
    while condition == True:

        #Update travel time
        G = update_travel_time_lpr(G, alpha, beta)

        # Initialize flow from OD Matrices, do shortest path
        # and calculate auxiliary flow.
        G = OD_shortest_path(G, nodes, flow, flow_type='auxflow')

        # line search using bisection method
        alpha = bisection(G, alpha=alpha, beta=beta)
        if n > number_of_iteration:
            condition = False
        alpha_old = alpha
        #updating mainflow based on optimal move size and auxflow
        G = update_mainflow(G, alpha)
        n+=1
        print(n)
    return G