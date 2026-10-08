from body import Body

G=6.67*10**-11
dt=0.1
bodies=[]
coordRange = [-10000,10000]
massRange = [10**-10,10**30]
vRange = [-3*10**8,3*10**8]
aRange = [-10**10,10**10]
#change to bounds

#add a body to the simulation 
def addBody(name,x,y,m,vx,vy):
    global coordRange
    global massRange
    global vRange
    inputs = [(x,coordRange),(y,coordRange),(m,massRange),(vx,vRange),(vy,vRange)]
    if all(validateInput(val,range) for val, range in inputs):
        newBody = Body(name,x,y,m,vx,vy)
        bodies.append(newBody)
    else:
        print("invalid input, try again")

#calculate the body forces and apply them by updating the positions.
def step(bodies,G,dt):
    for i in range(len(bodies)):
        for j in range(len(bodies)):
            if i!=j:
                dx=bodies[j].getX()-bodies[i].getX()
                dy=bodies[j].getY()-bodies[i].getY()
                distSq=(dx**2+dy**2)+0.0000000000000001 #softening factor
                dist=distSq**0.5
                f = (G*bodies[i].getM()*bodies[j].getM())/distSq
                fx = f*(dx/dist)
                fy = f*(dy/dist)
                bodies[i].setAX(bodies[i].getAX()+(fx/bodies[i].getM()))
                bodies[i].setAY(bodies[i].getAY()+(fy/bodies[i].getM()))
    for i in range(len(bodies)):
        bodies[i].update(dt)

#check if an input is numeric
def isNumeric(value):
    try: 
        float(value)
        return True
    except ValueError:
        return False

#validate inputs
def validateInput(value, range):
    if not isNumeric(value):
        return False
    elif value < range[0] or value > range[1]:
        return False
    else:
        return True

#get a body object by the name of it
def getBody(name):
    for body in bodies:
        if body.getName() == name:
            return body
    return None

#remove a body from the simulation
def removeBody(name):
    selectedBody = getBody(name)
    if selectedBody is None:
        return
    else:
        confirmation = input("do you want to remove this body? (y/n): ")
        if confirmation.lower() == "y":
            bodies.remove(selectedBody)
            #display()

#edit a body within the simulation
def editPos(name,newX,newY):
    selectedBody=getBody(name)
    if selectedBody is None:
        return
    else:
        if validateInput(newX,coordRange) and validateInput(newY,coordRange):
            selectedBody.setXY(newX,newY)
        else:
            print("invalid input, try again")

def editM(name,newM):
    selectedBody=getBody(name)
    if selectedBody is None:
        return
    else: 
        if validateInput(newM,massRange):
            selectedBody.setM(newM)
        else:
            print("invalid input, try again")

def editV(name,newVX,newVY):
    selectedBody=getBody(name)
    if selectedBody is None:
        return
    else:
        if validateInput(newVX,vRange) and validateInput(newVY,vRange):
            selectedBody.setV(newVX,newVY)
        else:
            print("invalid input, try again")


def loadPreset(presetChoice):
    global bodies
    bodies.clear()
    simulationTime=0
    #camera.reset()

    match presetChoice:
        case "Earth-Moon":
            addBody("Earth",0, 0, 8000000, 0, 0)
            addBody("Moon",400, 0, 1000000, 0, -141)
        case "Binary Star":
            addBody("Star1",-200, 0, 5000000, 0, -100)
            addBody("Star2",200, 0, 5000000, 0, 100)
        case "Three Bodies":
            addBody("Body1",0, -200, 3000000, 100, 0)
            addBody("Body2",200, 100, 3000000, -50, -80)
            addBody("Body3",-200, 100, 3000000, -50, 80)

#add comments g

#turn each attribute into a line of a save file so it can be read later to be loaded in
def saveCurrent(filename):
    if bodies == []:
        print("nothing to save")
        return
    saveFile = open(f"{filename}.txt","w")
    for body in bodies:
        for attribute in body.getAttributes():
            saveFile.write(str(attribute)+"\n")
    saveFile.close()
    print("saved successfully")

#load a save file by reading each line and turning each into attributes
def loadSaved(filename):
    saveFile = open(f"{filename}.txt","r")
    while True:
        name = saveFile.readline().strip()
        if not name:
            break
        x=float(saveFile.readline())
        y=float(saveFile.readline())
        m=float(saveFile.readline())
        vx=float(saveFile.readline())
        vy=float(saveFile.readline())
        ax=float(saveFile.readline())
        ay=float(saveFile.readline())
        addBody(name,x,y,m,vx,vy)
    saveFile.close() #had to close file to prevent corruption