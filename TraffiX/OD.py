import networkx as nx
import pandas as pd
import osmnx as ox

def OD_nodes_list(nodes_OD):
    for index, origin in nodes_OD.items():
        for index, dests in nodes_OD.items():
            yield (origin,dests)

def OD_shortest_path(G, nodes_OD, flow_list, flow_type='flow'):
    nx.set_edge_attributes(G, 0, flow_type)
    nodes = pd.DataFrame(list(OD_nodes_list(nodes_OD)))
    routes = ox.shortest_path(G, nodes.iloc[:,0], nodes.iloc[:,1], weight="travel_time", cpus=None)
    for i in range(len(routes)):
        link_flow(G,routes, i, flow_list[i], flow_type)
    return G