import requests
from bs4 import BeautifulSoup
parentUrl = 'https://www.yahoo.com/'
import grape
from grape.general_graph import GeneralGraph
from grape.general_graph import nx
import pickle

graph = GeneralGraph()
graph.add_node(parentUrl)

c = 5

while c>=0:
    r = requests.get(parentUrl)
    soup = BeautifulSoup(r.content, 'html.parser')

    imgs = soup.findAll('img')
    anchorTags = soup.findAll('a')

    sources = [imgs[i]['src'] for i in range(0, len(imgs))]
    for i in range(0, len(anchorTags)):
        if anchorTags[i]['href'] not in set(graph.nodes):
            graph.add_edge(parentUrl, anchorTags[i]['href'])
    edges = list(nx.breadth_first_search.bfs_edges(graph, source=parentUrl))
    bfsNodes = [v for u, v in edges]
    for child in bfsNodes:
        if 'https' in child:
            parentUrl = child
            r = requests.get(parentUrl)
            soup = BeautifulSoup(r.content, 'html.parser')
            imgs.extend(soup.findAll('img'))
            anchorTags = soup.findAll('a')
            
            for i in range(0, len(anchorTags)):
                try:
                    if anchorTags[i]['href'] and anchorTags[i]['href'] not in set(graph.nodes):
                        graph.add_edge(parentUrl, anchorTags[i]['href'])
                except:
                    pickle.dump(graph, open('./graph_progress.pickle', 'wb'))
                    continue
        else:
            continue
    c-=1