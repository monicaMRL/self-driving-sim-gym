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
    def __init__(self,verties,width,number,lane_type):
        self.vertices = verties
        self.color = [128,128,128]
        self.number = number
        self.type = lane_type
        
       
        self._markerWidth = 6
        self._markerLen = 50
        self._markerGap = 30
        self._markerNum = WIDTH / (self._markerLen + self._markerGap)
        self.markerList = list()
        
        self.bushList = list()
       
        for i in range(self._markerNum + 1):
            if self.type == 'h':
                v1 = [self.vertices[0][0] + i * (self._markerLen + self._markerGap) , self.vertices[0][1]  + self._markerWidth/2 ]#+ i * (self._markerLen + self._markerGap) ]
                v2 = [self.vertices[0][0] + i * (self._markerLen + self._markerGap) , self.vertices[0][1]  - self._markerWidth/2 ]
                v3 = [v2[0] + self._markerLen, self.vertices[0][1]  - self._markerWidth/2]
                v4 = [v2[0] + self._markerLen, self.vertices[0][1]  + self._markerWidth/2 ]
            
            
            elif self.type == 'v':
                v1 = [self.vertices[1][0] - self._markerWidth/2, self.vertices[1][1] + i * (self._markerLen + self._markerGap) ]
                v2 = [self.vertices[1][0] + self._markerWidth/2, self.vertices[1][1] + i * (self._markerLen + self._markerGap) ]
                v3 = [self.vertices[1][0] + self._markerWidth/2, v2[1] + self._markerLen ]
                v4 = [self.vertices[1][0] - self._markerWidth/2, v2[1] + self._markerLen ]
            
            self.marker_vertices = [v1,v2,v3,v4]
            marker = pygame.draw.polygon(displaySurface, [255,255,255], self.marker_vertices)
            self.markerList.append(marker)
            
            bush_img = pygame.image.load('bush.png')
            bush_img = pygame.transform.scale(bush_img, (64, 64))
            bush_rect = bush_img.get_rect()
            
            if self.number == 1 and self.type == 'h':                
                bush_rect.center = [v1[0],v1[1]-80]
            if self.number == -1:
                bush_rect.center = [v1[0],v1[1]+80]
                
            #bush_rect.center = tuple([bush_rect.center[0],bush_rect.center[1] + i*self._bushgap])
            self.bushList.append([bush_img,bush_rect])
        
            
    def _calculateVertices(self):
        v1 = self.corner
        v2 = [self.corner[0]+self.width,self.corner[1]]
        v3 = [v2[0],HEIGHT]
        v4 = [self.corner[0],HEIGHT]
        return [v1,v2,v3,v4]
        
    def relative_move(self,vel):
        #print len(self.markerList)
        new_obj = list()
        
        if self.type == 'h':
            for m in self.markerList:
                o = m.move(1 * vel[0], vel[1])
                
                if o.left < 0:
                    o.left =  WIDTH
                    
                new_obj.append(o)
                
        elif self.type == 'v':
            for m in self.markerList:
                o = m.move(vel[1], -1 * vel[0])
            
                if o.top > HEIGHT:
                    o.top = o.top % HEIGHT
                
                new_obj.append(o)
            
        self.markerList = new_obj
        
class Obstacles(object):
    def __init__(self,image_name,position,angle):
        self.image_name = image_name
        self.img = pygame.image.load(image_name)
        self.boundingBox = self.img.get_rect()
        self.boundingBox.center = position
        
        self.speed = 0
        self.streeAngle = 0
        self.heading = angle
        
        self.img = pygame.transform.rotate(self.img, self.heading)
        self.boundingBox = self.img.get_rect(center=self.boundingBox.center)
        
        #self.img, self.boundingBox = self.rot_center(self.img,self.boundingBox,self.heading)
        
        
    def rot_center(self,image, rect, angle):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image,rot_rect
        
    def move(self,velocity):
        self.boundingBox.move_ip(velocity)

        
class Agent(Obstacles):
    def __init__(self,image_name,position,angle):
        super(self.__class__, self).__init__(image_name,position,angle)

        
#----------------------- Class variables for enviroment -------------------------
#l1 = Lane([[0,150],[0,100],[WIDTH,100],[WIDTH,150]],50,1,'h')
l2 = Lane([[0,200],[0,150],[WIDTH,150],[WIDTH,200]],50,1,'h')
l3 = Lane([[0,250],[0,200],[WIDTH,200],[WIDTH,250]],50,0,'h')
l1 = Lane([[250,0],[300,0],[300,HEIGHT],[250,HEIGHT]],50,1,'v')
l4 = Lane([[300,0],[350,0],[350,HEIGHT],[300,HEIGHT]],50,0,'v')
l5 = Lane([[250,150],[350,150],[350,250],[250,250]],50,0,'v')
#l4 = Lane([[0,300],[0,250],[WIDTH,250],[WIDTH,300]],50,4,'h')
lane_list = [l2,l3,l1,l4]

robot = Agent('car1.png',[80,180],90)

o1 = Obstacles('car2.png',[150,230],90)
o2 = Obstacles('car2.png',[270,100],0)

obj_list = [o1,o2]
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

#            for bl in self.lane_list[0].bushList:
#                displaySurface.blit(bl[0], bl[1])
#                
#            for br in self.lane_list[-1].bushList:
#                displaySurface.blit(br[0], br[1])
        
        for l in self.lane_list:
                pygame.draw.polygon(displaySurface, l.color, l.vertices)
                
        for i in range(0,len(self.lane_list)):
            if lane_list[i].number == 1:
                for m in self.lane_list[i].markerList:
                        pygame.draw.rect(displaySurface, [255,255,255], m)
        
        pygame.draw.polygon(displaySurface, l5.color, l5.vertices)
        displaySurface.blit(self.agent.img, self.agent.boundingBox)
        
        for o in self.obj_list:
            displaySurface.blit(o.img, o.boundingBox)
            
        self._renderFlag = True
        pygame.display.update()
        
    def step(self,action):
#        for l in lane_list:
#            l.relative_move([-8,0])
        self.agent.move([9,0])
        o1.move([5,0])
        o2.move([0,2])
        
        if o1.boundingBox.center[0] > WIDTH:
            o1.boundingBox.center = [o1.boundingBox.center[0] % WIDTH,o1.boundingBox.center[1]]
        
        if self.agent.boundingBox.center[0] > WIDTH:
            self.agent.boundingBox.center = [self.agent.boundingBox.center[0] % WIDTH,self.agent.boundingBox.center[1]]
            
        if o2.boundingBox.center[1] > HEIGHT:
            o2.boundingBox.center = [o2.boundingBox.center[0],o2.boundingBox.center[1] % HEIGHT]
            
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
    
    
    
    