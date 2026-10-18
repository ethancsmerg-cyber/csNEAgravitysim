from body import Body
from simulation import *
from renderer import *

#create point
#Point = Body(1,2,3,4,5)
#test getters and setters
'''
print(Point.getX())
print(Point.getY())
print(Point.getM())
print(Point.getTrail())
Point.setX(100)
print(Point.getX())

p1 = Body(0, 0, 100, 0, 0)
p2 = Body(100, 0, 100, 0, 0)
bodies=[p1,p2]
G = 1000
dt = 0.1


#Symmetric accleration test
[print(body.getCoord()) for body in bodies]
p1.applyG(p2)
p1.update()
p2.update()
[print(body.getCoord()) for body in bodies]


#test for const acceleration
for i in range(1,6):
    p1.applyG(p2,G)
    print(f"Step{i}: p1 acceleration={p1.getA()}")
    print(f"Step{i}: p2 acceleration={p2.getA()}")
    [body.update(dt) for body in bodies]
    print(f"Step{i}: p1 coord={p1.getCoord()}")
    print(f"Step{i}: p2 coord={p2.getCoord()}")

#test for step
bodies = [Body(0,0,100,0,0), Body(100,0,100,0,0)]
G = 1000
dt = 0.1

for i in range(1,6):
    step(bodies, G, dt)
    print(f"Step {i}: p1 coord={[round(a,2) for a in bodies[0].getCoord()]} p2 coord={[round(a,2) for a in bodies[1].getCoord()]}")

#3 body test
bodies = [Body(0,0,100,0,0), Body(100,0,100,0,0), Body(50,100,100,0,0)]
G = 1000
dt = 0.1

for i in range(1,6):
    step(bodies, G, dt)
    print(f"Step {i}: p1={[round(x,2) for x in bodies[0].getCoord()]} p2={[round(x,2) for x in bodies[1].getCoord()]} p3={[round(x,2) for x in bodies[2].getCoord()]}")

#validateInput/isNumeric test
print(validateInput(100, coordRange))      #True
print(validateInput(-100, coordRange))     #True
print(validateInput(20000, coordRange))    #False
print(validateInput(-20000, coordRange))   #False
print(validateInput(0, massRange))         #False
print(validateInput(100, massRange))       #True
print(validateInput("hello", coordRange))  #False
print(validateInput(10000, coordRange))    #True
print(validateInput(-10000, coordRange))   #True



#addBody test with multiple bodies
for i in range(1,6):
    addBody(f"body{i}",i,i,i,i,i)

#removeBody test
for body in bodies:
    print(body.getAttributes())
removeBody("body3")


for body in bodies:
    print(body.getAttributes())
#editPos tests
editPos("body1",11,11)
editPos("body2",-11000,0)
editPos("body3",0,0)
editPos("body4",44,44)
for body in bodies:
    print(body.getAttributes())

#editM test
addBody("Earth", 0, 0, 100, 0, 0)
earth = getBody("Earth")
print(earth.getM())

editM("Earth", 500)        
print(earth.getM()) 

editM("Earth", -100)       
print(earth.getM())

editM("Earth", 0)          
print(earth.getM())

#editV test
addBody("Earth", 0, 0, 100, 0, 0)
earth = getBody("Earth")
print(earth.getV())

editV("Earth", 50, -50)    
print(earth.getV())

editV("Earth", 4*10**8, 0) 
print(earth.getV())

editV("Earth", "fast", 0)  
print(earth.getV())


#preset loadPreset, saveCurrent, loadSaved test
presetChoice = "Binary Star"
loadPreset(presetChoice)
print([body.getAttributes() for body in bodies])
print(bodies)
saveCurrent("test")
bodies.clear()
print(bodies)
loadSaved("test")
print(bodies)


#drawBody test
addBody("Test",0,0,1*10**6,0,0)

camX,camY=0,0
zoom=1.0
screen=pygame.display.set_mode((WIDTH,HEIGHT))
screen.fill(BLACK)


for body in bodies:
    drawBody(screen, body, camX, camY, zoom)

pygame.display.flip()
pygame.time.wait(3000)
pygame.quit()
'''

run()  