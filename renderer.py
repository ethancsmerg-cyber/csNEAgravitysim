import pygame
from simulation import *

#define display 
WIDTH, HEIGHT = 1440,1080
FPS = 60

#define basic colours
BLACK=(0,0,0)
WHITE=(255,255,255)
YELLOW=(255,255,0)
RED=(255,0,0)

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

class inputBox:
    def __init__(self,x,y,width,height,label,default=""):
        self.rect=pygame.Rect(x,y,width,height)
        self.label=label
        self.text=str(default)
        self.active=False
        self.colour=WHITE

    def draw(self,screen,font):
        labelText = font.render(self.label, True, WHITE)
        screen.blit(labelText, (self.rect.x, self.rect.y - 25))
        colour = YELLOW if self.active else WHITE
        pygame.draw.rect(screen, (30, 30, 30), self.rect)
        pygame.draw.rect(screen, colour, self.rect, 2)
        text = font.render(self.text, True, WHITE)
        screen.blit(text, (self.rect.x + 5, self.rect.y + 5))

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
                self.text += event.unicode

    def getValue(self):
        try:
            return float(self.text)
        except ValueError:
            return None

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
    addMode=False
    removeMode=False
    editMode=False
    btnW,btnH=180,45
    btnX=10
    addPanel=None
    editPanel=None
    buttons={
        "add": Button(btnX,160,btnW,btnH,"Add Body"),
        "remove": Button(btnX,220,btnW,btnH,"Remove Body"),
        "edit": Button(btnX,280,btnW,btnH,"Edit Body")
    }
    backspaceHeld = 0
    backspaceDelay = 30 
    backspaceInterval = 3 
    last_click_time=0
    threshold=500
    followed_body=None
    pending_body=None
    delete_buttons={}
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked_hud_delete=False
                    for body,rect in delete_buttons.items():
                        if rect.collidepoint(event.pos):
                            pending_body=body
                            clicked_hud_delete=True
                    if pending_body:
                        x=WIDTH//2-200
                        y=HEIGHT//2-100
                        yes_rect=pygame.Rect(x+50,y+120,100,40)
                        no_rect=pygame.Rect(x+250,y+120,100,40)

                        if yes_rect.collidepoint(event.pos):
                            removeBody(pending_body)
                            if followed_body==pending_body:
                                followed_body=None
                            pending_body=None
                            clicked_hud_delete=True
                        elif no_rect.collidepoint(event.pos):
                            pending_body=None
                            clicked_hud_delete=True
                            
                    current_time = pygame.time.get_ticks()
                    mouseX,mouseY=event.pos
                    if current_time-last_click_time<threshold:
                        for body in bodies:
                            screenX,screenY=worldToScreen(body.getX(),body.getY(),camX,camY,zoom,WIDTH,HEIGHT)
                            r = max(calculateRadius(body.getM()) * zoom, 10)
                            dsq=(mouseX-screenX)**2+(mouseY-screenY)**2
                            d=math.sqrt(dsq)
                            if d<=r:
                                clicked_body=body
                        if clicked_body:
                            if followed_body==clicked_body:
                                followed_body=None
                            else:
                                followed_body=clicked_body
                        else:
                            clicked_body=None
                    else:
                        last_click_time=current_time 
                    if buttons["add"].isClicked(event.pos):
                        addMode = not addMode
                        removeMode=False
                        editMode=False
                    elif buttons["remove"].isClicked(event.pos):
                        removeMode = not removeMode
                        addMode=False
                        editMode=False
                    elif buttons["edit"].isClicked(event.pos):
                        editMode=not editMode
                        addMode=False
                        removeMode=False
                    elif removeMode:
                        mouseX,mouseY=event.pos
                        body_to_remove=None
                        for body in bodies:
                            screenX,screenY=worldToScreen(body.getX(),body.getY(),camX,camY,zoom,WIDTH,HEIGHT)
                            r = max(calculateRadius(body.getM()) * zoom, 10)
                            dsq=(mouseX-screenX)**2+(mouseY-screenY)**2
                            d=math.sqrt(dsq)
                            if d<=r:
                                body_to_remove=body 
                        if body_to_remove:
                            removeBody(body_to_remove)
                    elif editMode and not editPanel:
                        mouseX,mouseY=event.pos
                        body_to_edit=None
                        for body in bodies:
                            screenX,screenY=worldToScreen(body.getX(),body.getY(),camX,camY,zoom,WIDTH,HEIGHT)
                            r = max(calculateRadius(body.getM()) * zoom, 10)
                            dsq=(mouseX-screenX)**2+(mouseY-screenY)**2
                            d=math.sqrt(dsq)
                            if d<=r:
                                body_to_edit=body
                        if body_to_edit:
                            panelX=WIDTH//2-150
                            panelY=HEIGHT//2-200
                            editPanel = {
                                    "name": inputBox(panelX, panelY + 50, 300, 40, "Name:", body_to_edit.getName()),
                                    "x":    inputBox(panelX, panelY + 130, 300, 40, "X:", body_to_edit.getX()),
                                    "y":    inputBox(panelX, panelY + 210, 300, 40, "Y:", body_to_edit.getY()),
                                    "m":    inputBox(panelX, panelY + 290, 300, 40, "Mass:", body_to_edit.getM()),
                                    "vx":   inputBox(panelX, panelY + 370, 300, 40, "VX:", body_to_edit.getV()[0]),
                                    "vy":   inputBox(panelX, panelY + 450, 300, 40, "VY:", body_to_edit.getV()[1]),
                                    "confirm": Button(panelX, panelY + 520, 140, 45, "Confirm"),
                                    "cancel":  Button(panelX + 160, panelY + 520, 140, 45, "Cancel"),
                                }
                if event.button == 3 and addMode:  # right click in add mode
                    mouseX, mouseY = event.pos
                    worldX = round((mouseX - WIDTH // 2) / zoom + camX,2)
                    worldY = round((mouseY - HEIGHT // 2) / zoom + camY,2)
                    panelX=WIDTH//2-150
                    panelY=HEIGHT//2-200
                    addPanel={
                        "name": inputBox(panelX, panelY + 50, 300, 40, "Name:", "New Body"),
                        "x":    inputBox(panelX, panelY + 130, 300, 40, "X:", worldX),
                        "y":    inputBox(panelX, panelY + 210, 300, 40, "Y:", worldY),
                        "m":    inputBox(panelX, panelY + 290, 300, 40, "Mass:", 1000000),
                        "vx":   inputBox(panelX, panelY + 370, 300, 40, "VX:", 0),
                        "vy":   inputBox(panelX, panelY + 450, 300, 40, "VY:", 0),
                        "confirm": Button(panelX, panelY + 520, 140, 45, "Confirm"),
                        "cancel":  Button(panelX + 160, panelY + 520, 140, 45, "Cancel"),
                    }
            if addPanel:
                for key, box in addPanel.items():
                    if isinstance(box, inputBox):
                        box.handleEvent(event)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if addPanel["confirm"].isClicked(event.pos):
                        name = addPanel["name"].text
                        x = addPanel["x"].getValue()
                        y = addPanel["y"].getValue()
                        m = addPanel["m"].getValue()
                        vx = addPanel["vx"].getValue()
                        vy = addPanel["vy"].getValue()
                        if all(k is not None for k in [x, y, m, vx, vy]):
                            addBody(name, x, y, m, vx, vy)
                        addPanel = None
                        addMode = False
                    if addPanel and addPanel["cancel"].isClicked(event.pos):
                        addPanel = None
                        addMode = False
            if editPanel:
                for key,box in editPanel.items():
                    if isinstance(box,inputBox):
                        box.handleEvent(event)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if editPanel["confirm"].isClicked(event.pos):
                        newName = editPanel["name"].text
                        newX = editPanel["x"].getValue()
                        newY = editPanel["y"].getValue()
                        newM = editPanel["m"].getValue()
                        newVX = editPanel["vx"].getValue()
                        newVY = editPanel["vy"].getValue()
                        if all(k is not None for k in [newX, newY, newM, newVX, newVY]):
                            body_to_edit.setName(newName)
                            editPos(body_to_edit,newX,newY)
                            editM(body_to_edit,newM)
                            editV(body_to_edit,newVX,newVY)
                        editPanel = None
                        editMode = False
                    if editPanel and editPanel["cancel"].isClicked(event.pos):
                        editPanel = None
                        editMode = False
                
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
        activePanel=addPanel if addPanel else editPanel
        if activePanel:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_BACKSPACE]:
                backspaceHeld += 1
                if backspaceHeld == 1 or (backspaceHeld > backspaceDelay and backspaceHeld % backspaceInterval == 0):
                    for box in activePanel.values():
                        if isinstance(box, inputBox) and box.active:
                            box.text = box.text[:-1]
            
        else:
            backspaceHeld = 0
        if followed_body:
            if followed_body in bodies:
                camX=followed_body.getX()
                camY=followed_body.getY()
            else:
                followed_body=None
        if not paused:
            for i in range(n):
                step(bodies,G,dt)
        screen.fill(BLACK)
        for body in bodies:
            drawTrail(screen,body,camX,camY,zoom)
            drawBody(screen,body,camX,camY,zoom)
        mousePos = pygame.mouse.get_pos()
        if addPanel:
            panelX = WIDTH // 2 - 150
            panelY = HEIGHT // 2 - 200
            pygame.draw.rect(screen, (20, 20, 20), (panelX - 20, panelY, 340, 600))
            pygame.draw.rect(screen, WHITE, (panelX - 20, panelY, 340, 600), 2)
            titleText = font.render("Add Body", True, YELLOW)
            screen.blit(titleText, (panelX, panelY + 10))
            for key, box in addPanel.items():
                box.draw(screen, font)
        for button in buttons.values():
            button.update(mousePos)
            button.draw(screen,font)

        if editPanel:
            panelX = WIDTH // 2 - 150
            panelY = HEIGHT // 2 - 200
            pygame.draw.rect(screen, (20, 20, 20), (panelX - 20, panelY, 340, 600))
            pygame.draw.rect(screen, WHITE, (panelX - 20, panelY, 340, 600), 2)
            titleText = font.render("Edit Body", True, YELLOW)
            screen.blit(titleText, (panelX, panelY + 10))
            for key, box in editPanel.items():
                box.draw(screen,font)
        for button in buttons.values():
            button.update(mousePos)
            button.draw(screen,font)
        #print("blitting text")
        pauseText = font.render("PAUSED" if paused else "RUNNING", True, WHITE)
        screen.blit(pauseText, (50, 100))
        controlsText = font.render("SPACE: pause | 1/2/3: presets | WASD: pan | scroll: zoom", True, WHITE)
        screen.blit(controlsText, (140,100))
        delete_buttons=drawInfoPanel(screen,bodies,font)
        
        if addMode:
            hintText = font.render("Right click to place body", True, YELLOW)
            screen.blit(hintText, (500,100))
        if removeMode:
            hintText=font.render("REMOVE MODE ACTIVE",True,RED)
            screen.blit(hintText,(500,100))
        if editMode:
            hintText=font.render("EDIT MODE ACTIVE",True,YELLOW)
            screen.blit(hintText,(500,100))
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
    button_rects={}
    for body in bodies:
        nameText = font.render(body.getName(), True, YELLOW)
        screen.blit(nameText, (x, y))
        name_width = nameText.get_width()
        del_rect=pygame.Rect(x+name_width+10,y,20,20)
        pygame.draw.rect(screen,RED,del_rect,border_radius=3)
        del_text=font.render("X",True,WHITE)
        screen.blit(del_text,(del_rect.x+6,del_rect.y+1))
        button_rects[body]=del_rect

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
    return button_rects