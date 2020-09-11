# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 09:36:03 2020

@author: PranabGhosh
"""
import math
import numpy as np
from get_bar_info import get_bar_info
from extract_text_info import extract_text_info
import pandas as pd

LEGENDS = {"Blue":"LA Zoo", "Orange":"SF Zoo"}

def get_scale(axis):
    all_scale = []
    for i,y in enumerate(axis[1:]):
        if y[0].isdigit() and axis[i-1][0].isdigit():
            sc = abs(y[1][1]-axis[i-1][1][1])/abs(float(y[0])-float(axis[i-1][0]))
            all_scale.append(sc)
    avg_scale = sum(all_scale)/len(all_scale)
    return avg_scale

def map_xAxis(coords,hor_axis):
    distItem = []
    for hItem in hor_axis:
        distItem.append([hItem[0],math.sqrt(pow(coords[0]-hItem[1][0],2)+pow(coords[1]-hItem[1][1],2))])
    distItem.sort(key=lambda x:x[1])
    return distItem[0][0]        


#INPUT FILE PATH
image_path = 'vert_bar_graph_1.jpg'

text_info, vert_axis, hor_axis = extract_text_info(image_path)

bar_info = get_bar_info(image_path)

y_scale = get_scale(vert_axis)

for bi,b_info in enumerate(bar_info):
    by = int((b_info[1][3])/y_scale)
    bar_info[bi].append(by)
    bar_info[bi][0] = LEGENDS[bar_info[bi][0]]
    bar_info[bi].append(map_xAxis(b_info[1],hor_axis))

hAxis = [h[0] for h in hor_axis]

cols = ["LA Zoo", "SF Zoo"]

data_array = np.zeros((len(hAxis),len(cols)))

for b_info in bar_info:
    h_idx = hAxis.index(b_info[3])
    v_idx = cols.index(b_info[0])
    data_array[h_idx,v_idx] = b_info[2]
    
dataframe = pd.DataFrame(data_array,columns=cols)
dataframe.insert(0,"",hAxis)

dataframe.to_csv(image_path[:-4]+'.csv')