#import pygame
from simulation import *

WIDTH, HEIGHT = 800,600
FPS = 60

BLACK=(0,0,0)
WHITE=(255,255,255)
YELLOW=(255,255,0)

def calculateRadius(m):
    return max(3, int(m**0.3))

print(calculateRadius(30))

def worldToScreen(x,y,camX,camY,zoom,width,height):
    screenX=int((x-camX)*zoom+width//2)
    screenY=int((y-camY)*zoom+height//2)
    return screenX,screenY
