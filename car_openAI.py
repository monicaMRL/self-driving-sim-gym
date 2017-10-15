# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 00:08:48 2017

@author: monica
"""

#--------------------------------- Imports ----------------------------------------------------
import pygame
import matplotlib.path as mplPath
import numpy as np
import math
import time
import copy
from scipy.spatial.distance import euclidean as point_dist

#------------------- Global Variables ------------------------------------------------------------------

WIDTH = 500
HEIGHT = 500
FPS = 40

lastAngle = 0

pygame.init()
displaySurface = pygame.display.set_mode((WIDTH,HEIGHT))
mainClock = pygame.time.Clock()
pygame.display.set_caption('Traffic World')
pygame.display.update()

#------------------------------ Classes ----------------------------------------------------------

class Lane(object):
    def __init__(self,corner,width,number):
        self.width = width
        self.corner = corner
        self.vertices = self._calculateVertices()
        self.color = [128,128,128]
        self.number = number
        
        self.bound_l = [self.corner,[self.corner[0],HEIGHT]]
        self.bound_r = [[self.corner[0]+self.width,self.corner[1]],[self.corner[0]+self.width,HEIGHT]]
        self.bound_color = [0,0,0]

        self.lane_rect = pygame.draw.polygon(displaySurface, self.color, self.vertices)        
        
        self._markerWidth = 6
        self._markerLen = 50
        self._markerGap = 30
        self._markerNum = HEIGHT / (self._markerLen + self._markerGap)
        self.markerList = list()
        
        self.bushList = list()
       
        for i in range(self._markerNum + 1):
            v1 = [self.bound_r[0][0] - self._markerWidth/2, self.bound_r[0][1] + i * (self._markerLen + self._markerGap) ]
            v2 = [self.bound_r[0][0] + self._markerWidth/2, self.bound_r[0][1] + i * (self._markerLen + self._markerGap) ]
            v3 = [self.bound_r[0][0] + self._markerWidth/2, v2[1] + self._markerLen ]
            v4 = [self.bound_r[0][0] - self._markerWidth/2, v2[1] + self._markerLen ]
            
            self.marker_vertices = [v1,v2,v3,v4]
            marker = pygame.draw.polygon(displaySurface, [255,255,255], self.marker_vertices)
            self.markerList.append(marker)
            
            bush_img = pygame.image.load('bush.png')
            bush_img = pygame.transform.scale(bush_img, (64, 64))
            bush_rect = bush_img.get_rect()
            
            if self.number == 1:                
                bush_rect.center = [v1[0]-80,v1[1]]
            if self.number == 4:
                bush_rect.center = [v1[0]+80,v1[1]]
                
            #bush_rect.center = tuple([bush_rect.center[0],bush_rect.center[1] + i*self._bushgap])
            self.bushList.append([bush_img,bush_rect])
        
            
    def _calculateVertices(self):
        v1 = self.corner
        v2 = [self.corner[0]+self.width,self.corner[1]]
        v3 = [v2[0],HEIGHT]
        v4 = [self.corner[0],HEIGHT]
        return [v1,v2,v3,v4]
        
    def relative_move(self,vel):
        
        new_obj = list()
        
        for m in self.markerList:
            o = m.move(vel[0], -1 * vel[1])
            
            if o.top > HEIGHT:
                o.top = o.top % HEIGHT
                
            new_obj.append(o)
            
        self.markerList = new_obj
        
        
class Obstacles(object):
    def __init__(self,image_name,position,angle,initial_speed):
        self.image_name = image_name

        self.img = pygame.image.load(image_name)
        self.mutable_img = self.img.copy()
        
        self.boundingBox = self.img.get_rect()
        self.boundingBox.center = position
        self.mutable_bb = copy.deepcopy(self.boundingBox)
        
        self.speed = initial_speed
        self.heading = angle
        self.last_heading = 0
        
    def move(self,speed,heading):
        
        self.speed = speed
        self.heading = heading
        
        y = self.speed * math.cos(math.radians(self.heading))
        x = self.speed * math.sin(math.radians(self.heading))
        
        #print self.heading, self.last_heading
        
        if not self.heading == self.last_heading:
            self.mutable_img = pygame.transform.rotate(self.img, -self.heading)
            self.mutable_bb = self.mutable_img.get_rect(center=self.mutable_bb.center)
            #self.boundingBox = self.mutable_img.get_rect(center=self.boundingBox.center)
            self.last_heading = self.heading
            
        #self.boundingBox.move_ip([x,y])
        self.mutable_bb.move_ip([x,y])

        
class Agent(Obstacles):
    def __init__(self,image_name,position,angle,init_speed):
        super(self.__class__, self).__init__(image_name,position,angle,init_speed)
        
    def move(self,speed,heading):
        self.speed = speed
        self.heading = heading
        
        y = 0
        x = self.speed * math.sin(math.radians(self.heading))
        
        if not self.heading == self.last_heading:
            self.mutable_img = pygame.transform.rotate(self.img, -self.heading)
            self.mutable_bb = self.mutable_img.get_rect(center=self.mutable_bb.center)
            #self.boundingBox = self.mutable_img.get_rect(center=self.boundingBox.center)
            self.last_heading = self.heading
            
        #self.boundingBox.move_ip([x,y])
        self.mutable_bb.move_ip([x,y])
   
#----------------------- Class variables for enviroment -------------------------
l1 = Lane([100,0],50,1)
l2 = Lane([150,0],50,2)
l3 = Lane([200,0],50,3)
l4 = Lane([250,0],50,4)
lane_list = [l1,l2,l3,l4]

robot = Agent('car1.png',[230,HEIGHT-30],0,6)

o1 = Obstacles('car2.png',[230,130],180,5)

obj_list = [o1]

#---------------------- Environment----------------------------------------------

class Environment(object):
    def __init__(self,lane_list,obj_list,agent):
        self.lane_list = lane_list
        self.obj_list = obj_list
        self.agent = agent
        
        self._renderFlag = False
        self._renderObj()
        
        self.maxAcc = 5
        self.distance = 0
        self.maxAngle = 90
        
    def _renderObj(self):
        displaySurface.fill((154,205,50))

        for bl in self.lane_list[0].bushList:
            displaySurface.blit(bl[0], bl[1])
            
        for br in self.lane_list[3].bushList:
            displaySurface.blit(br[0], br[1])
        
        for l in self.lane_list:
                pygame.draw.rect(displaySurface, l.color, l.lane_rect)
                
        for i in range(0,len(self.lane_list)-1):
            for m in self.lane_list[i].markerList:
                    pygame.draw.rect(displaySurface, [255,255,255], m)
        
        #displaySurface.blit(self.agent.mutable_img, self.agent.boundingBox)
        displaySurface.blit(self.agent.mutable_img, self.agent.mutable_bb)
        
        for o in self.obj_list:
            #displaySurface.blit(o.img, o.boundingBox)
            displaySurface.blit(o.img, o.mutable_bb)

        #self._renderFlag = True
        pygame.display.update()
        
    def check_collision(self):
    	print "Inside collision checker \n"
        rect_list = list()
        
        for o in self.obj_list:
            rect_list.append(o.mutable_bb)

        collision = self.agent.mutable_bb.collidelist(rect_list)
        
        if collision >= 0:
        	collision = True
    	else:
    		collision = False
        
        return collision
        
    def in_laneNumber(self):
        for l in self.lane_list:
        	test_result = l.lane_rect.contains(self.agent.mutable_bb)
        	#print test_result
        	if test_result == True:
        		return l.number
        return None
        
            
    def step(self,action):
        """
        action is list with acceleration and steering angle
        """
        acc = action[0] * self.maxAcc
        steerAngle = action[1] * self.maxAngle
        
        self.agent.speed += acc
        self.agent.heading += steerAngle        
        
        print self.agent.heading
        print self.in_laneNumber()

        
    def step_visual(self):
        
        for l in lane_list:
            l.relative_move([0,-self.agent.speed])
            
        o1.move(o1.speed,math.pi)
        
        self.agent.move(self.agent.speed,self.agent.heading)
    
        if o1.mutable_bb.center[1] > HEIGHT:
            o1.mutable_bb.center = [o1.mutable_bb.center[0],o1.mutable_bb.center[1] % HEIGHT]
        
        elif o1.mutable_bb.center[1] < 0:
            o1.mutable_bb.center = [o1.mutable_bb.center[0],HEIGHT]

        if self.check_collision():
        	print "CRASSSSSSSHHHHHHHHH"

 
        self._renderObj()
        mainClock.tick(FPS)
        
        
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
                    init_steer = - 0.1
                elif event.key == pygame.K_RIGHT:                    
                    init_steer = 0.1
                elif event.key == pygame.K_UP:                    
                    init_acc = 0.1
                elif event.key == pygame.K_DOWN:
                    init_acc = - 0.1
                else:
                    print "No keys"
                    curr_action = None
    
                env.step([init_acc,init_steer])

        env.step_visual()        
        mainClock.tick(FPS)
        
    pygame.quit()
    quit()
    
    
    
    