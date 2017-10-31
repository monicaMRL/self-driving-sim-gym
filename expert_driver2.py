# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 03:36:29 2017

@author: monica
"""

from car_openAI import *


if __name__ == '__main__':
    env = Environment(lane_list,obj_list,robot)
    gameExit = False
    init_acc = 0
    init_steer = 0
    intended_heading = 0

    while not gameExit:
        next_state,observation,done = env.step([init_acc,init_steer])
        
        angle = intended_heading - observation[1]
#        add_change = round(observation[4+2],4)
#        angle += add_change
        
        print "Distance from green opp: ", observation[12],observation[10]
        print "Distance from green opp: ", observation[11],observation[9]
        
        if observation[12] < 100 and (observation[3] == 2 or observation[3] == -1):
            add_change = round(observation[4+2],4)
            angle += add_change
            
        elif observation[11] < 100 and (observation[3] == 3 or observation[3] == -1):
            add_change = round(observation[4+1],4)
            angle += add_change
            
        init_steer = round(float(angle) / 360.0,4)
        
        if done:
            init_acc = 0
            init_steer = 0
            env.reset()
        
        print init_steer, observation[1], observation[4], observation[3]
        
    	mainClock.tick(FPS)    

    pygame.quit()
    quit()
    