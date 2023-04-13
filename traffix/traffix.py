import osmnx as ox
import pandas as pd
import networkx as nx
import numpy as np


def add_edge_lanes(G, lanes_min=1):
    """
    Add default lanes towards NaN lanes value in edge attributes.
    It also change lanes column type into numeric.
    
    By default, this imputes 1 lane toward existing NaN values.
    
    Parameters
    ----------
    G : networkX.MultiDiGraph
        input graph
    lanes_min : int
        assigning minimum values to be inserted.
    """
    #Check if lanes_min is integer
    if not isinstance(lanes_min, int):
        raise TypeError(
            (
                "lanes_min type must be an integer."
            )
        )
    
    edges = ox.utils_graph.graph_to_gdfs(G, nodes=False, fill_edge_geometry=False)
    
    #Change all list values in lanes colum into maximum value of lanes
    #in that list.
    edges["lanes"] = [int(max(x)) if isinstance(x, list) else x for x in edges['lanes']]
    
    #Impute missing values with lanes value.
    lanes = (
        edges[["highway", "lanes"]].set_index("highway").iloc[:, 0].fillna(lanes_min)
    )
    edges["lanes"] = lanes.values
    
    #Change lanes column into numeric
    edges['lanes']=pd.to_numeric(edges['lanes'])
    nx.set_edge_attributes(G, values=edges["lanes"], name="lanes")
    
    return G

def add_edge_width(G, width_min=3.5):
    """
    Add default width towards NaN width value in edge attributes.
    
    By default, this imputes 3.5 meters toward existing NaN values.
    
    Parameters
    ----------
    G : networkX.MultiDiGraph
        input graph
    width_min : int
        assigning minimum values to be inserted.
    """
    #Check if width_min is float
    if not isinstance(width_min, (float,int)):
        raise TypeError(
            (
                "width_min type must be an integer or float."
            )
        )
    
    edges = ox.utils_graph.graph_to_gdfs(G, nodes=False, fill_edge_geometry=False)
    
    #Change all list values in lanes colum into maximum value of lanes
    #in that list.
    edges["width"] = [int(max(x)) if isinstance(x, list) else x for x in edges['width']]
    
    #Impute missing values with width value.
    width = (
        edges[["highway", "width"]].set_index("highway").iloc[:, 0].fillna(width_min)
    )
    #Change lanes column into numeric
    edges["width"]=pd.to_numeric(edges["width"])
    edges["width"] = width.values
    nx.set_edge_attributes(G, values=edges["width"], name="width")
    
    return G

def add_edge_capacity(G, base_capacity=None, fallback=1650):
    """
    Add edge capacity to graph as new "capacity" edge attributes.
    
    By default, this imputes 1650 * number of lane toward existing 
    NaN values.
    
    Parameters
    ----------
    G : networkX.MultiDiGraph
        input graph
    base_capacity : dict
        dict keys = OSM highway types and values = typical capacity
        to assign to edges of that highway type for any edges missing
        capacity data. Any edges with highway type not in `base_capacity` 
        will be assigned the fallback value.
    fallback : numeric
        default capacity value to assign to edges whose highway
        type did not appear in `base_capacity`. Default value is based on
        Indonesian Higway Capacity Manual 1997 (MKJI 1997).
    """
    
    edges = ox.utils_graph.graph_to_gdfs(G, nodes=False, fill_edge_geometry=False)

    # collapse any highway lists (can happen during graph simplification)
    # into string values simply by keeping just the first element of the list
    edges["highway"] = edges["highway"].map(lambda x: x[0] if isinstance(x, list) else x)
    edges["capacity"] = None
    # if user provided base_capacity, use them as default values, otherwise
    # initialize an empty series to populate with fallback values.
    if base_capacity is None:
        capacity_avg = pd.Series(dtype=float).fillna(fallback)
    else:
        capacity_avg = pd.Series(base_capacity).dropna()
    
    # for each highway type that caller did not provide in base_capacity, impute
    # capacity of type by using fallback values
    for cap, group in edges.groupby("highway"):
        if cap not in capacity_avg:
            capacity_avg.loc[cap] = fallback
    
    #Impute missing values with lanes value.
    capacity = (
        edges[["highway", "capacity"]].set_index("highway").iloc[:, 0].fillna(capacity_avg)
    )
    edges["capacity"] = capacity.round(0).values * edges["lanes"]
    nx.set_edge_attributes(G, values=edges["capacity"], name="capacity")
    
    return G

def flatten_osmid(G):
    df = ox.graph_to_gdfs(ox.project_graph(G), nodes=False)
    #Flatten the osmid, can happen during simplification.
    df['osmid'] = df['osmid'].map(lambda x: x[0] if isinstance(x, list) else x).values
    df["highway"] = df["highway"].map(lambda x: x[0] if isinstance(x, list) else x).values
    nx.set_edge_attributes(G, df['osmid'], name='osmid')
    nx.set_edge_attributes(G, df["highway"], name="highway")
    return G  

def add_edge_initial_travel_time(G):
    df = nx.to_pandas_edgelist(G, edge_key='ekey').set_index(["source","target","ekey"])
    df['initial_travel_time'] = df['travel_time'].values
    nx.set_edge_attributes(G, df['initial_travel_time'], name='initial_travel_time')
    return G  

def Flow_from_OD(OD):
    OD.index += 1
    OD.columns = list(range(1,len(OD.index)+1))
    if not len(OD.index) == len(OD.columns):
        raise IndexError(
            (
                "The number of origin and destination must be the same."
            )
        )
    for origin in range(1,len(OD.index)+1):
        for dests in range(1,len(OD.columns)+1):
            if origin == dests:
                yield origin,dests,0
            else:
                flow = OD.iloc[origin-1 ,OD.columns.get_loc(dests)]
                yield origin,dests,flow

def link_flow(G, routes, k, flow, flow_type):
    t = 'travel_time'
    if routes[k] is None:
        return G
    else:
        for i in range(len(routes[k])-1):
            minimum = G[routes[k][i]][routes[k][i+1]][0][t]
            j = 0
            keys = 0
            for j in range(len(G.get_edge_data(routes[k][i], routes[k][i+1]))):
                if G.get_edge_data(routes[k][i], routes[k][i+1], j)[t] < minimum:
                    minimum = G.get_edge_data(routes[k][i], routes[k][i+1], j)[t]
                    keys = j
            link_flow = flow + G[routes[k][i]][routes[k][i+1]][keys][flow_type]
            attrs = {(routes[k][i], routes[k][i+1], keys): {flow_type: link_flow}}
            nx.set_edge_attributes(G, attrs)
        return G

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