import pygame
from simulation import *

#define display 
WIDTH, HEIGHT = 800,600
FPS = 60

#define basic colours
BLACK=(0,0,0)
WHITE=(255,255,255)
YELLOW=(255,255,0)

#find the radius of a body according to mass
def calculateRadius(m):
    return max(3, int((m ** 0.3)/10)) #scale this later in development

#print(calculateRadius(30))

def worldToScreen(x,y,camX,camY,zoom,width,height):
    screenX=int((x-camX)*zoom+width//2)
    screenY=int((y-camY)*zoom+height//2)
    return screenX,screenY
'''
print(worldToScreen(0, 0, 0, 0, 1, 800, 600))
print(worldToScreen(100, 0, 0, 0, 1, 800, 600))  
print(worldToScreen(0, 100, 0, 0, 1, 800, 600))
print(worldToScreen(0, 0, 100, 0, 1, 800, 600)) 
print(worldToScreen(0, 0, 0, 0, 2, 800, 600))  
print(worldToScreen(100, 0, 0, 0, 2, 800, 600)) 
'''

def drawBody(screen,body,camX,camY,zoom):
    screenX,screenY=worldToScreen(body.getX(),body.getY(),camX,camY,zoom,WIDTH,HEIGHT)
    r=calculateRadius(body.getM())
    pygame.draw.circle(screen,YELLOW,(screenX,screenY),r)

def run():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Gravity Simulator")
    clock = pygame.time.Clock()

    camX,camY=0,0
    zoom=0.3 #cahnged this from 1.0 add into documentation
    loadPreset("Earth-Moon")
    print(bodies)
    running=True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False

        step(bodies,G,dt)

        screen.fill(BLACK)
        for body in bodies:
            drawBody(screen, body,camX,camY,zoom)

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


