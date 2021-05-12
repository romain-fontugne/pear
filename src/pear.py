from as_graph import ASGraph
import pickle

prefix_weights = {'1.1.1.0/24':1, '8.8.8.0/24':8, '9.9.9.0/24':9}

graph = ASGraph('2021-05-01T00:00', 2497, 'route-views.wide')
graph.build_graph()
graph.propagate_prefix_weight(prefix_weights)

with open('iij_graph.pickle', 'wb') as fp:
    pickle.dump(graph, fp)
