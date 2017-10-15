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
    
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit == True
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    init_steer -=  0.1
                elif event.key == pygame.K_RIGHT:                    
                    init_steer += 0.1
                elif event.key == pygame.K_UP:                    
                    init_acc += 0.1
                elif event.key == pygame.K_DOWN:
                    init_acc -=  0.1
                else:
                    print "No keys"
                    init_acc = 0
                    init_steer = 0

    		print "-----------------",init_acc, init_steer

        next_state,observation,done = env.step([init_acc,init_steer])
        if done:
            env.reset()

        print observation
    	
    	mainClock.tick(FPS)    

    pygame.quit()
    quit()
    