import pickle
from grape.general_graph import nx

graph_obj = pickle.load(open('./graph_progress.pickle', 'rb'))

print(graph_obj)