# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 21:22:35 2020

@author: PranabGhosh
"""
import cv2
from copy import deepcopy
from pytesseract import image_to_boxes

def extract_text_info(img_path):
    img = cv2.imread(img_path,0)    
    
    tess_out = image_to_boxes(img,config='--psm 6 --oem 2')
    
    tess_char_data = tess_out.split('\n')
    
    tess_char_info = []
    
    for tcd in tess_char_data:
        tess_char_info.append([tcd[0],[int(dd) for dd in tcd[2:].split()][:-1]])
    
    tess_word_info = [deepcopy(tess_char_info[0])]
    for tci in tess_char_info[1:]:
        if abs(tci[1][0]-tess_word_info[-1][1][2])<=10 and abs(tci[1][3]-tess_word_info[-1][1][3])<10:
            tess_word_info[-1][0] += tci[0]
            tess_word_info[-1][1][2] = tci[1][2]
        else:
            tess_word_info.append(deepcopy(tci))
    
      
    vert_sorted_words = deepcopy(tess_word_info)
    vert_sorted_words.sort(key=lambda x:x[1][0])
    
    hor_sorted_words = deepcopy(tess_word_info)
    hor_sorted_words.sort(key=lambda x:x[1][1])
    
    vert_sorted_groups = [[vert_sorted_words[0]]]
    for vtw in vert_sorted_words[1:]:
        if abs(vtw[1][2]-vert_sorted_groups[-1][-1][1][2])<5:
            vert_sorted_groups[-1].append(vtw)
        else:
            vert_sorted_groups.append([vtw])
            
    hor_sorted_groups = [[hor_sorted_words[0]]]
    for htw in hor_sorted_words[1:]:
        if abs(htw[1][1]-hor_sorted_groups[-1][-1][1][1])<5:
            hor_sorted_groups[-1].append(htw)
        else:
            hor_sorted_groups.append([htw])
            
    vert_axis = sorted(vert_sorted_groups,key=lambda x:-len(x))[0]
    hor_axis = sorted(hor_sorted_groups,key=lambda x:-len(x))[0]
    vert_axis.sort(key=lambda x:x[1][1])
    hor_axis.sort(key=lambda x:x[1][0])
    return tess_word_info, vert_axis, hor_axis

#img_path = 'C:/Users/ManasiDhekane/Desktop/Trainings/CognitiveDigitazion/vert_bar_graph_1.jpg'
#tess_word_info, vert_axis, hor_axis = extract_text_info(img_path)