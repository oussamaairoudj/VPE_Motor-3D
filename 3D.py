import pygame
import numpy as np
from math import sqrt,cos,sin,log
from pygame import K_z,K_s,K_q,K_d,K_w,K_x,K_e,K_r

WIDTH, HEIGHT = 1000, 600
pygame.init()
pygame.display.set_caption('3D System Solaire')
font=pygame.font.SysFont("monospace",15)
screen = pygame.display.set_mode((WIDTH,HEIGHT))
planet_data = [
    [[WIDTH/2, HEIGHT/2,10],[0, 0,0],1000000,(255,255,0)],
    [[620, 100,20],[-5, 5,10],300,(255,0,0)],
    [[740, 500,80],[5,-5,7],400,(0,0,255)],
    [[200, 240,30],[5,10,-4],100,(0,255,0)],
    [[300, 240,60],[5,-10,0],300,(0,255,255)],
    [[660, 140,10],[-5,-10,0],200,(255,0,255)]
]
dt = 0.3
rotation=[0,0,0]
focus=800

class Planet():
    def __init__(self,p,sp,m,c):
        self.pos=p
        self.speed=sp
        self.mass=m
        self.color=c
        self.force=[0,0,0]
        self.queues=[]

    def show(self,x,y):
        pygame.draw.circle(screen,self.color,(x,y),log(self.mass)+5)
        planet.force=[0,0,0]
        pygame.display.update()

def norm(v):
    nv = sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    return [v[0]/nv, v[1]/nv, v[2]/nv]

def dist(v1, v2):
    return sqrt((v1[0]-v2[0])**2 + (v1[1]-v2[1])**2 + (v1[2]-v2[2])**2)

def mul_v(a, v):
    return [a*v[0], a*v[1], a*v[2]]

def add_v(v1, v2):
    return [v1[0]+v2[0], v1[1]+v2[1], v1[2]+v2[2]]

def forces():
    k = 0.1
    for i in planets:
        for j in planets:
            if i != j:
                f = k*i.mass*j.mass / dist(i.pos, j.pos)**2
                u = norm([j.pos[0] - i.pos[0], j.pos[1] - i.pos[1], j.pos[2] - i.pos[2]])
                i.force = add_v(i.force, mul_v(f, u))

def Rx(angle):
    return [[1,0,0],[0,cos(angle),-sin(angle)],[0,sin(angle),cos(angle)]]

def Ry(angle):
    return [[cos(angle),0,sin(angle)],[0,1,0],[-sin(angle),0,cos(angle)]]

def Rz(angle):
    return [[cos(angle),-sin(angle),0],[sin(angle),cos(angle),0],[0,0,1]]

def Camra(pos,angle,focus):
    def projection(z):
        return [[z,0,0],[0,-z,0]]
    rot=np.dot(Rx(angle[0]),pos)
    rot=np.dot(Ry(angle[1]),rot)
    rot=np.dot(Rz(angle[2]),rot)
    z=200/(focus+rot[2])
    return np.dot(projection(z),rot)+[400,300]

planets=[Planet(*data)for data in planet_data]
angle=0.05
params = {
        K_z: (0, angle),
        K_s: (0, -angle),
        K_q: (1, angle),
        K_d: (1, -angle),
        K_w: (2, angle),
        K_x: (2, -angle),
        K_e: (50),
        K_r: (-50)
    }

while True:
    screen.fill(0)
    screen.blit(font.render('Angle Camera : '+str(rotation),1,(250,0,0)),(10,10))
    screen.blit(font.render('Focus Camera : '+str(focus),1,(250,0,0)),(10,30))
    screen.blit(font.render('Les Buttons : (A,S): pour Rd-X , (Q,D): pour Rd-Y , (W,X): pour Rd-Z , (E,R): pour Focus Camera  ',1,(250,0,0)),(10,570))
    pygame.time.Clock().tick(40)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        for key in params:
            if pygame.key.get_pressed()[key]:
                if key == 101 or key == 114:
                    focus+=params[key]
                else:
                    rotation[params[key][0]]+=params[key][1]
    forces()
    for planet in planets:
        planet.speed=add_v(planet.speed,mul_v(dt,mul_v(1/planet.mass,planet.force)))
        planet.pos=add_v(planet.pos,mul_v(dt,planet.speed))
        planet.queues.append(planet.pos)
        for q in planet.queues[-90:]:
            pygame.draw.circle(screen,planet.color,Camra(q,rotation,focus),1)
        planet.show(*Camra(planet.pos,rotation,focus))
