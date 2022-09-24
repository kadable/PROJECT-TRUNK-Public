"""
This file contians global functions and all the imports. 
Every file imports this.
"""
import pygame
import csv
import math
import sys
import random
import json

#General Functions
#Returns sign
def sign(num):
    if num == 0:
        return 0
    elif num > 0:
        return 1
    elif num < 0:
        return -1
    
#Clamps between 2 numbers
def clamp(num,min_num,max_num):
    return max(min_num,min(num,max_num))
def delete_duplicates_from_list(list_x):
  return list(dict.fromkeys(list_x))

#Frames is a 2d array with image name and duration
#Current frame is a list with index and current time
#Returns new current frame
def animation(frames,current_frame,loop=True):
    if current_frame[1] >= frames[current_frame[0]][1]:
        if current_frame[0] >= len(frames)-1:
            if loop:
                current_frame = [0,0]
            else:
                return False
        else:
            current_frame = [current_frame[0]+1,0]
    else:
        current_frame[1] += 1
    return current_frame

def switch_animation(current_animation,new_animation,current_frame,new_frame=[0,0],switch_always=False):
    if current_animation != new_animation or switch_always:
        return new_animation, new_frame
    else:
        return current_animation,current_frame
