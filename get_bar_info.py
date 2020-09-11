# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 12:00:15 2020

@author: PranabGhosh
"""

import cv2
import math

COLORS = {"Blue":(255,0,0),"Orange":(0, 128, 255)}

def get_color(img):
    ih,iw,_ = img.shape
    rgb_values = []
    for i in range(ih):
        for j in range(iw):
            rgb_values.append((img[i,j,0],img[i,j,1],img[i,j,2]))
    
    color = most_frequent(rgb_values)
    dist_list = []
    for c,cv in COLORS.items():
        cd = math.sqrt(pow(cv[0]-color[0],2)+pow(cv[1]-color[1],2)+pow(cv[2]-color[2],2))
        dist_list.append([c,cd])
    dist_list.sort(key=lambda x:x[1])
    color = dist_list[0][0]
    return color

def most_frequent(List): 
    counter = 0
    num = List[0] 
      
    for i in List: 
        curr_frequency = List.count(i) 
        if(curr_frequency> counter): 
            counter = curr_frequency 
            num = i 
  
    return num 
    
def get_bar_info(img_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    img_height,img_width = gray.shape
    
    cv2.imshow('img',gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    ret,thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    cv2.imshow('img',thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    _,contours,h = cv2.findContours(thresh,1,2)
    
    bars = []
    
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        if len(approx)==4 and 200<cv2.contourArea(cnt)<(img_width*img_height)//3:
            cv2.drawContours(img,[cnt],-1, (0,0,0), 3)
            bbox = cv2.boundingRect(cnt)
            color = get_color(img[bbox[1]+10:bbox[1]+20,bbox[0]+10:bbox[0]+20,:])
            bars.append([color,bbox])
    
    bars.sort(key=lambda x:x[1][0])  
    
    cv2.imshow('img',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return bars

#img_path = 'C:/Users/ManasiDhekane/Desktop/Trainings/CognitiveDigitazion/vert_bar_graph_1.jpg'
#basr_info = get_bar_info(img_path)