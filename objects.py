import pygame as pg
import random
import math
from settings import *
vec=pg.Vector2
class Blob:
    def __init__(self,pos,r):
        self.pos=vec(pos)
        self.radius=r
        angle=random.uniform(0,math.pi*2)
        self.vel=vec(math.cos(angle),math.sin(angle))*random.randint(50,100)
    def update(self,dt):
        self.pos+=self.vel*dt
        if self.pos.x>WIDTH or self.pos.x<0:
            self.vel.x*=-1
        if self.pos.y>HEIGHT or self.pos.y<0:
            self.vel.y*=-1
    def show(self,surf):
        pg.draw.circle(surf,WHITE,self.pos,self.radius,1)
