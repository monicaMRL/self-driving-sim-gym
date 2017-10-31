# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 20:40:58 2017

@author: monica
"""

import math
import copy

def move2lane(ob,lane_number):
    add_change = round(ob[4+lane_number-1],4)
    
    return add_change
    
def change_lane(ob, change_direction):
    """
    distance from lane index: 1:4 2:5 3:6 4:7
    """
    cur_lane = ob[3]
    
    if change_direction == 'left':
        go2lane = cur_lane - 1
    elif change_direction == 'right':
        go2lane = cur_lane + 1
    else:
        go2lane = cur_lane
        
    if go2lane > 4 or go2lane < 1:
        go2lane = cur_lane
        
    return move2lane(ob,go2lane)