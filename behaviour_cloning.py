# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 01:11:44 2017

@author: monica
"""

from sklearn.neighbors import KDTree
from sklearn.neighbors import KNeighborsRegressor
import pickle
import numpy as np

from car_openAI import *
from behaviours import *

data_file = open("expert_data_2.pkl","rb")
data = None
X = list()
Y = list()

while(True):
    try:
        data = pickle.load(data_file)
    except EOFError:
        break
       
for ele in data:
    X.append(ele[0])
    Y.append(ele[1])
    
X = np.array(X)
Y = np.array(Y)

print X.shape, Y.shape

neigh = KNeighborsRegressor(n_neighbors=5)
neigh.fit(X,Y)

if __name__ == '__main__':
    env = Environment(lane_list,obj_list,robot)
    gameExit = False
    init_acc = 0
    init_steer = 0
    intended_heading = 0
    count = 0

    while not gameExit:
        next_state,observation,done = env.step([init_acc,init_steer])
        ob = np.array(observation)
        ob = ob[:,np.newaxis].T
        
        op = neigh.predict(ob)
        
        init_acc = op[0][0]
        init_steer = op[0][1]
        
        if done:
            init_acc = 0
            init_steer = 0
            env.reset()
        
    	mainClock.tick(FPS)    

    pygame.quit()
    quit()
    


