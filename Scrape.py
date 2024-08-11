import requests
from bs4 import BeautifulSoup
import grape
from grape.general_graph import nx
import pickle

parentUrl = 'https://www.yahoo.com/'
graph = nx.Graph()
graph.add_node(parentUrl)

c = 5

def find_tag(url:str, tagName:str='a'):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        tagList = soup.findAll(tagName)
        return tagList
    except:return

def track_and_add_attribute(srcNode:str, tagList:list, graphObj:nx.Graph, attr:str = 'href'):
    for i in range(0, len(tagList)):
        if tagList[i][attr] and 'http' in tagList[i][attr]:
            graphObj.add_edge(srcNode, tagList[i][attr])

def url_bfs_traversal(graphObj:nx.Graph, srcNode:str):
    edges = nx.breadth_first_search.bfs_edges(graphObj, source=srcNode)
    bfs_nodes = [v for u, v in edges]
    for node in bfs_nodes:
        tagList = find_tag(node)
        
        if tagList: track_and_add_attribute(srcNode=node, tagList=tagList, graphObj=graphObj)
        pickle.dump(graph, open('./graph_progress.pickle', 'wb'))
        
        url_bfs_traversal(graphObj=graph, srcNode=node)
        pickle.dump(graph, open('./graph_progress.pickle', 'wb'))

while c>=0:
    tagList = find_tag(parentUrl)
    if tagList: track_and_add_attribute(srcNode=parentUrl, tagList=tagList, graphObj=graph)
    url_bfs_traversal(graphObj=graph, srcNode=parentUrl)
    c-=1
    pickle.dump(graph, open('./graph_progress.pickle', 'wb'))

pickle.dump(graph, open('./graph_progress.pickle', 'wb'))
