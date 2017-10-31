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
import random

#------------------- Global Variables ------------------------------------------------------------------

WIDTH = 500
HEIGHT = 500
FPS = 15

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
        self.middle = corner[0] + self.width/2.0
        self.vertices = self._calculateVertices()
        self.color = [128,128,128]
        self.number = number
        
        self.bound_l = [self.corner,[self.corner[0],HEIGHT]]
        self.bound_r = [[self.corner[0]+self.width,self.corner[1]],[self.corner[0]+self.width,HEIGHT]]
        self.bound_color = [0,0,0]

        self.lane_rect = pygame.draw.polygon(displaySurface, self.color, self.vertices)        
        
        self._markerWidth = 10
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
                bush_rect.center = [30,v1[1]]
            if self.number == 4:
                bush_rect.center = [WIDTH-30,v1[1]]
                
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
            o = m.move(vel[0], vel[1])
            
            if o.top > HEIGHT:
                o.top = o.top % HEIGHT

            elif o.top < 0:
                o.top = HEIGHT

            new_obj.append(o)
            
        self.markerList = new_obj
        
        
class Obstacles(object):
    def __init__(self,image_name,position,angle,initial_speed):
        self.image_name = image_name
        self.img = pygame.image.load(image_name)
        self.img = pygame.transform.scale(self.img,(45,45))
        self.mutable_img = self.img.copy()
        
        self.boundingBox = self.img.get_rect()
        self.boundingBox.center = position
        self.mutable_bb = copy.deepcopy(self.boundingBox)
        
        self.speed = initial_speed
        self.heading = angle
        self.last_heading = 0
        
        
    def appear_random(self,flag):
        if flag == 'p':
            opp_P = [[275,0],[180,0],[130,0],[400,0]]
        else:
            opp_P = [[275,HEIGHT],[180,HEIGHT],[130,HEIGHT],[400,HEIGHT]]
            
        random_in = random.randint(0,len(opp_P)-1)
        
        return opp_P[random_in]
        
        
        
    def move(self,speed,heading):
        
        self.speed = speed

        if not heading > 90:
        	self.heading = heading 
        
        y = self.speed * round(math.cos(math.radians(self.heading)),4)
        x = self.speed * round(math.sin(math.radians(self.heading)),4)
        
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
        self.img = pygame.transform.scale(self.img,(45,45))
        self.mutable_img = self.img.copy()
        
        self.boundingBox = self.img.get_rect()
        self.boundingBox.center = position
        self.mutable_bb = copy.deepcopy(self.boundingBox)
        
        
        
    def move(self,speed,heading):
        self.speed = speed

        if not heading > 90:
        	self.heading = heading
        
        y = 0
        x = self.speed * round(math.sin(math.radians(self.heading)),4)
        
        if not self.heading == self.last_heading:
            self.mutable_img = pygame.transform.rotate(self.img, -self.heading)
            self.mutable_bb = self.mutable_img.get_rect(center=self.mutable_bb.center)
            #self.boundingBox = self.mutable_img.get_rect(center=self.boundingBox.center)
            self.last_heading = self.heading
            
        #self.boundingBox.move_ip([x,y])
        self.mutable_bb.move_ip([x,y])
   
#----------------------- Class variables for enviroment -------------------------
l1 = Lane([50,0],100,1)
l2 = Lane([150,0],100,2)
l3 = Lane([250,0],100,3)
l4 = Lane([350,0],100,4)

lane_list = [l1,l2,l3,l4]

agent_initP = [180,HEIGHT-100]
agent_initA = 20
agent_initS = 8
robot = Agent('car_ver.png',agent_initP,agent_initA,agent_initS)

opp_P = [[275,0],[180,0],[130,0],[400,0]]

opp1_P = [275,130]
opp1_A = 0
opp1_S = 3

opp2_P = [400,130]
opp2_A = 0
opp2_S = 2

opp3_P = [130,130]
opp3_A = 0
opp3_S = 2

opp4_P = [180,130]
opp4_A = 0
opp4_S = 2

o1 = Obstacles('opp_ver.png',opp1_P,opp1_A,opp1_S)
o2 = Obstacles('opp_g.png',opp2_P,opp2_A,opp2_S)
o3 = Obstacles('opp_g.png',opp3_P,opp3_A,opp3_S)
o4 = Obstacles('opp_ver.png',opp4_P,opp4_A,opp4_S)

obj_list = [o1,o2,o3,o4]

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
#         test_result = l.lane_rect.contains(self.agent.mutable_bb)
         test_result = l.lane_rect.collidepoint(self.agent.mutable_bb.center)
         
         if test_result:
             dist = l.lane_rect.center[0] - self.agent.mutable_bb.center[0]
             number = l.number
             return number, -dist
             
        return None
    
    def in_laneNumGen(self,rect):

        for l in self.lane_list:
        	test_result = l.lane_rect.contains(rect)
        	
        	if test_result == True: 
        		return l.number, 
        return None
    


    def off_road(self):
    	
        off_roadFlag = False
        
        agent_right = self.agent.mutable_bb.right
        agent_left = self.agent.mutable_bb.left
        rightMost = self.lane_list[-1].lane_rect.right
        leftMost = self.lane_list[-0].lane_rect.left


        if agent_right > rightMost or agent_left < leftMost:
            off_roadFlag = True
	

        return off_roadFlag


    def reset(self):
        self.agent.mutable_bb.center = self.agent.boundingBox.center
        self.agent.heading = agent_initA
        self.agent.speed = agent_initS
        
        o1.mutable_bb.center = o1.boundingBox.center
        o1.heading = opp1_A
        o1.speed = opp1_S

        o2.mutable_bb.center = o2.boundingBox.center
        o2.heading = opp2_A
        o2.speed = opp2_S  
     

    def step(self,action):
        """
        action is list with acceleration and steering angle
        0: Next_speed           8:off_road
        1: Next_Heading         9-10: for opponante lane Number
        2: Lane_angle           11-12: distance from opponent
        3: Lane_number
        4-7: distance from lane 1 2 3 4
        """
        # next_speed, next_heading, lane_angle, lane_number,all_lane distance from center, off_road, opp_laneNum, opp_dist 
        observation = list()
        done = False

        acc = round(action[0],4) * self.maxAcc
        steerAngle = round(action[1],4) * self.maxAngle
        
        old_speed = self.agent.speed
        
        self.agent.speed += acc
        self.agent.heading += steerAngle
        
        if self.agent.speed < 0:
            self.agent.speed = old_speed
        
        if self.agent.heading > 0:
            self.agent.heading = self.agent.heading % 360
        elif self.agent.heading < 0:
            self.agent.heading = self.agent.heading % - 360
            
        observation.append(round(self.agent.speed,3))
        observation.append(round(self.agent.heading,3))
        observation.append(round(self.agent.heading,3))

        _ = self.in_laneNumber()
        
        if not _ == None:
            lane_number,dist_center = _#self.in_laneNumber()
            observation.append(lane_number)
            #observation.append(dist_center)
        else:
            observation.append(-1)
            #observation.append(50)
            
        for l in self.lane_list:
            dist = l.lane_rect.center[0] - self.agent.mutable_bb.center[0]
            observation.append(dist)
            
        off_roadFlag = self.off_road()

        if off_roadFlag:
            done = True
            observation.append(1)
        else:
            done = False
            observation.append(0)

        for on in self.obj_list:
            o_rect = on.mutable_bb
            o_laneNum = self.in_laneNumGen(o_rect)
            if not o_laneNum == None:
                observation.append(o_laneNum[0])
            else:
                observation.append(-100)
                
        for od in self.obj_list:
            o_rect = od.mutable_bb
            
            if not o_rect.center[1] > HEIGHT or o_rect.center[1] < 0:
                o_dist = point_dist(np.array(self.agent.mutable_bb.center),np.array(o_rect.center))
                observation.append(o_dist)
            else:
                observation.append(999)


        if self.agent.heading > 90 or self.agent.heading < -90:
            for l in lane_list:
                l.relative_move([0,-self.agent.speed])
        else:
            for l in lane_list:
                l.relative_move([0,self.agent.speed])

        self.agent.move(self.agent.speed,self.agent.heading)
            
        for o in self.obj_list:
            old_ospeed = o.speed
            o.speed += acc
            if o.speed < 0:
                o.speed = old_ospeed
            #if o.speed-self.agent.speed < 0:
                #o.move(o.speed,180)
            #else:
                #o.move(o.speed,0)
            o.move(o.speed,0)
                
            if o.mutable_bb.center[1] > HEIGHT:
                o.mutable_bb.center = o.appear_random('p')#[o.mutable_bb.center[0],o.mutable_bb.center[1] % HEIGHT]
            elif o.mutable_bb.center[1] < 0:
                o.mutable_bb.center = o.appear_random('n')
                
        collision_flag = self.check_collision()
        
        if collision_flag:
            done = True
       
        self._renderObj()

        return [self.agent.speed,self.agent.heading],observation, done
       
        
  