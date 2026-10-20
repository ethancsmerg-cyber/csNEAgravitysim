import pygame
from simulation import *

#define display 
WIDTH, HEIGHT = 1440,1080
FPS = 60

#define basic colours
BLACK=(0,0,0)
WHITE=(255,255,255)
YELLOW=(255,255,0)

class Button:
    def __init__(self, x, y, width, height, text, colour=(60,60,60), textColour=(255,255,255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.colour = colour
        self.textColour = textColour
        self.hovered = False

    def draw(self, screen, font):
        colour = (100,100,100) if self.hovered else self.colour
        pygame.draw.rect(screen, colour, self.rect, border_radius=5)
        pygame.draw.rect(screen, WHITE, self.rect, 1, border_radius=5)
        text = font.render(self.text, True, self.textColour)
        textRect = text.get_rect(center=self.rect.center)
        screen.blit(text, textRect)

    def update(self, mousePos):
        self.hovered = self.rect.collidepoint(mousePos)

    def isClicked(self, mousePos):
        return self.rect.collidepoint(mousePos)
    
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
    r=calculateRadius(body.getM())*zoom
    pygame.draw.circle(screen,YELLOW,(screenX,screenY),r)

n=1 #number of times step is called during run
def run():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Gravity Simulator")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 16) 
    camX,camY=0,0
    zoom=1.0 #cahnged this from 1.0 add into documentation
    loadPreset("Stationary Central Body")
    print(bodies)
    paused = False
    running=True
    btnW,btnH=180,45
    btnX=10
    buttons={
        "add": Button(btnX,160,btnW,btnH,"Add Body")
    }
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if buttons["add"].isClicked(event.pos):
                        addMode = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if event.key == pygame.K_1:
                    loadPreset("Stationary Central Body")
                if event.key == pygame.K_2:
                    loadPreset("Binary Star")
                if event.key == pygame.K_3:
                    loadPreset("Three Bodies")
            if event.type == pygame.MOUSEWHEEL:
                zoom += event.y * 0.1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            camX -= 10 / zoom
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            camX += 10 / zoom
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            camY -= 10 / zoom
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            camY += 10 / zoom
        if not paused:
            for i in range(n):
                step(bodies,G,dt)
        screen.fill(BLACK)
        for body in bodies:
            drawTrail(screen,body,camX,camY,zoom)
            drawBody(screen,body,camX,camY,zoom)
            mousePos = pygame.mouse.get_pos()
            for button in buttons.values():
                button.update(mousePos)
                button.draw(screen,font)
        #print("blitting text")
        pauseText = font.render("PAUSED" if paused else "RUNNING", True, WHITE)
        screen.blit(pauseText, (100, 100))
        controlsText = font.render("SPACE: pause | 1/2/3: presets | WASD: pan | scroll: zoom", True, WHITE)
        screen.blit(controlsText, (200,100))
        drawInfoPanel(screen,bodies,font)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


def drawTrail(screen,body,camX,camY,zoom):
    trail=body.getTrail()
    for i in range(len(trail)-1):
        x1,y1=worldToScreen(trail[i][0],trail[i][1],camX,camY,zoom,WIDTH,HEIGHT)
        x2,y2=worldToScreen(trail[i+1][0],trail[i+1][1],camX,camY,zoom,WIDTH,HEIGHT)
        pygame.draw.line(screen,WHITE,(x1,y1),(x2,y2),1)

def drawInfoPanel(screen,bodies,font):
    x=WIDTH-300
    y=100
    for body in bodies:
        nameText = font.render(body.getName(), True, YELLOW)
        screen.blit(nameText, (x, y))
        y += 30
        posText = font.render(f"pos: ({round(body.getX(),2)}, {round(body.getY(),2)})", True, WHITE)
        screen.blit(posText, (x, y))
        y += 30
        velText = font.render(f"vel: {int(math.sqrt(sum(x**2 for x in body.getV())))}ms-1, ({round(body.getVX(),2)}, {round(body.getVY(),2)})", True, WHITE)
        screen.blit(velText, (x, y))
        y += 30
        massText = font.render(f"mass: {body.getM():.2e}kg", True, WHITE)
        screen.blit(massText, (x, y))
        y += 50