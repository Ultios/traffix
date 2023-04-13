import networkx as nx
import numpy as np

def update_travel_time_lpr(G, alpha=0.15, beta=4):
    df = nx.to_pandas_edgelist(G, edge_key='ekey').set_index(["source","target","ekey"])
    df['travel_time'] = df.apply(lambda x: lpr(x, alpha, beta), axis=1).values
    nx.set_edge_attributes(G, df['travel_time'], name='travel_time')
    return G

#This is a link performance function derived from Indonesia's Highway Manual (MKJI 1997).
def lpr(row, alpha=0.15,beta=4):
    if np.isnan(row['flow']):
        return row['travel_time']
    else:
        try:
            return row['initial_travel_time']*(1+alpha*(row['flow']/row['capacity'])**beta)
        except ValueError:
            return row['travel_time']

