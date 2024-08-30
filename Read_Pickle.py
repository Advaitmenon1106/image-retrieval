import json
import pickle
from grape.general_graph import nx, plt
from bs4 import BeautifulSoup
import requests
import numpy as np, pandas as pd
import concurrent.futures

graph_obj = pickle.load(open('./graph_progress3.pickle', 'rb'))

def getImgs(urlArray:set[str]):
    tagLists = []
    imgLinks = []
    c = 0
    for url in urlArray:
        try:
            c+=1
            r = requests.get(url=url, timeout=10)
            soup = BeautifulSoup(r.content, 'html.parser')
            tagList = soup.findAll('img', recursive=True)

            tagLists.extend(tagList)

            if c%5 == 0 and c!=0:
                ser = pd.Series(tagLists)
                ser.to_csv('./taglist_csv.csv')

            print(f'Website #{c}')
                
        except:
            c-=1
            print('Failed, continuing.')
            continue
    
    print('processing tags')
    
    for tag in tagLists:
        if tag.has_attr('href') and 'http' in tag['href']:
            imgLinks.append(tag['href'])
    
    return imgLinks

imgs = getImgs(set(graph_obj.nodes))
print(len(imgs))
pickle.dump(imgs, open('./img.pickle', 'wb'))