import pygame
from simulation import *

#define display 
WIDTH, HEIGHT = 1440,1080
FPS = 60

#define basic colours
BLACK=(0,0,0)
WHITE=(255,255,255)
YELLOW=(255,255,0)

#find the radius of a body according to mass
def calculateRadius(m):
    return max(3, int((m ** 0.3)/5)) #scale this later in development

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

n=1 #number of times step is called during run
def run():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Gravity Simulator")
    clock = pygame.time.Clock()

    camX,camY=0,0
    zoom=1.0 #cahnged this from 1.0 add into documentation
    loadPreset("Earth-Moon")
    print(bodies)
    paused = False
    running=True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if event.key == pygame.K_1:
                    loadPreset("Earth-Moon")
                if event.key == pygame.K_2:
                    loadPreset("Binary Star")
                if event.key == pygame.K_3:
                    loadPreset("Three Bodies")
        if not paused:
            for i in range(n):
                step(bodies,G,dt)

        screen.fill(BLACK)
        for body in bodies:
            drawTrail(screen,body,camX,camY,zoom)
            drawBody(screen,body,camX,camY,zoom)
            

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


def drawTrail(screen,body,camX,camY,zoom):
    trail=body.getTrail()
    for i in range(len(trail)-1):
        x1,y1=worldToScreen(trail[i][0],trail[i][1],camX,camY,zoom,WIDTH,HEIGHT)
        x2,y2=worldToScreen(trail[i+1][0],trail[i+1][1],camX,camY,zoom,WIDTH,HEIGHT)
        pygame.draw.line(screen,WHITE,(x1,y1),(x2,y2),1)



