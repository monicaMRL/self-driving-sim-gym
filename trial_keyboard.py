# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 03:36:29 2017

@author: monica
"""

from car_openAI import *


speed = 3
actionSet = {'up':[0,-1*speed],'dw':[0,1*speed],'lf':[-1*speed,0],'rt':[1*speed,0]}

if __name__ == "__main__":
    env = Environment(lane_list,obj_list,robot)
    gameExit = False
    
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit == True
        env.step(None)
#            if event.type == pygame.KEYDOWN:
#                if event.key == pygame.K_LEFT:                    
#                    env.step(actionSet['lf'])
#                elif event.key == pygame.K_RIGHT:                    
#                    env.step(actionSet['rt'])
#                elif event.key == pygame.K_UP:                    
#                    env.step(actionSet['up'])
#                elif event.key == pygame.K_DOWN:
#                    env.step(actionSet['dw'])
#                else:
#                    print "No keys"
                
        
    pygame.quit()
    quit()