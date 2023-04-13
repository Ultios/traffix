import networkx as nx



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