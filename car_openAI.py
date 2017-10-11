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
from scipy.spatial.distance import euclidean as point_dist

#------------------- Global Variables ------------------------------------------------------------------

WIDTH = 500
HEIGHT = 500
FPS = 40

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
    def __init__(self,image_name,position):
        self.image_name = image_name
        self.img = pygame.image.load(image_name)
        self.boundingBox = self.img.get_rect()
        self.boundingBox.center = position
        
        self.speed = 0
        self.streeAngle = 0
        self.heading = 0
        
    def move(self,velocity):
        self.boundingBox.move_ip(velocity)

        
class Agent(Obstacles):
    def __init__(self,image_name,position):
        super(self.__class__, self).__init__(image_name,position)

        
#----------------------- Class variables for enviroment -------------------------
l1 = Lane([100,0],50,1)
l2 = Lane([150,0],50,2)
l3 = Lane([200,0],50,3)
l4 = Lane([250,0],50,4)
lane_list = [l1,l2,l3,l4]

robot = Agent('car1.png',[280,HEIGHT-30])

o1 = Obstacles('car2.png',[230,130])

obj_list = [o1]
#---------------------- Environment----------------------------------------------

class Environment(object):
    def __init__(self,lane_list,obj_list,agent):
        self.lane_list = lane_list
        self.obj_list = obj_list
        self.agent = agent
        
        self._renderFlag = False
        self._renderObj()
        
        
    def _renderObj(self):
        if self._renderFlag == False:
            displaySurface.fill((154,205,50))

            for bl in self.lane_list[0].bushList:
                displaySurface.blit(bl[0], bl[1])
                
            for br in self.lane_list[3].bushList:
                displaySurface.blit(br[0], br[1])
        
        for l in self.lane_list:
                pygame.draw.polygon(displaySurface, l.color, l.vertices)
                
        for i in range(0,len(self.lane_list)-1):
            for m in self.lane_list[i].markerList:
                    pygame.draw.rect(displaySurface, [255,255,255], m)
        
        displaySurface.blit(self.agent.img, self.agent.boundingBox)
        
        for o in self.obj_list:
            displaySurface.blit(o.img, o.boundingBox)
            
        self._renderFlag = True
        pygame.display.update()
        
    def step(self,action):
        for l in lane_list:
            l.relative_move([0,-8])
            
        o1.move([0,3])
        
        if o1.boundingBox.center[1] > HEIGHT:
            o1.boundingBox.center = [o1.boundingBox.center[0],o1.boundingBox.center[1] % HEIGHT]
        
        self._renderObj()
        mainClock.tick(FPS)
        
if __name__ == '__main__':
    env = Environment(lane_list,obj_list,robot)
    gameExit = False
    
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit == True
    
        env.step(None)
        mainClock.tick(FPS)
        
    pygame.quit()
    quit()
    
    
    
    