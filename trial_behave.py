# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 03:36:29 2017

@author: monica
"""

from car_openAI import *
from behaviours import *


if __name__ == '__main__':
    env = Environment(lane_list,obj_list,robot)
    gameExit = False
    init_acc = 0
    init_steer = 0
    intended_heading = 0
    count = 0

    while not gameExit:
        next_state,observation,done = env.step([init_acc,init_steer])
        
        angle = intended_heading - observation[1]

        if observation[3] > 1 or observation[3] == -1:
            add_change = change_lane(observation,'left')
            angle += add_change
        
        
        add_change = change_lane(observation,'center')
        angle += add_change
        
        init_steer = round(float(angle) / 360.0,4)
        
        if done:
            init_acc = 0
            init_steer = 0
            env.reset()
        
    	mainClock.tick(FPS)    

    pygame.quit()
    quit()
    