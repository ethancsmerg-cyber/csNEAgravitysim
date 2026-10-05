import tkinter as tk
import random




#Body class
class Body:
    def __init__(self,name,x,y,m,vx,vy):
        self.__name=name
        self.__x=x
        self.__y=y
        self.__m=m
        self.__vx=vx
        self.__vy=vy
        self.__ax=0
        self.__ay=0
        self.__trail=[]

    def __repr__(self):
        return f"{self.__name}(({self.__x},{self.__y}), m={self.__m:.2e}kg, v=({self.__vx},{self.__vy})ms-1, a=({self.__ax},{self.__ay})ms-2)" 
    
    #getter functions for the body's attributes
    def getAttributes(self):
        return [self.__name,self.__x,self.__y,self.__m,self.__vx,self.__vy,self.__ax,self.__ay]
    def getName(self):
        return self.__name
    def getX(self):
        return self.__x
    def getY(self):
        return self.__y
    def getM(self):
        return self.__m
    def getVX(self):
        return self.__vx
    def getVY(self):
        return self.__vy
    def getAX(self):
        return self.__ax
    def getAY(self):
        return self.__ay
    def getTrail(self):
        return self.__trail
    def getCoord(self):
        return [self.__x,self.__y]
    def getV(self):
        return [self.__vx,self.__vy]
    def getA(self):
        return [self.__ax,self.__ay]
        
    #setter functions for all attributes except trail    
    def setName(self,newName):
        self.__name=newName
    def setX(self,newX):
        self.__x=newX
    def setY(self,newY):
        self.__y=newY
    def setM(self,newM):
        self.__m=newM
    def setVX(self,newVX):
        self.__vx=newVX
    def setVY(self,newVY):
        self.__vy=newVY
    def setAX(self,newAX):
        self.__ax=newAX
    def setAY(self,newAY):
        self.__ay=newAY
    def setXY(self,newX,newY):
        self.__x=newX
        self.__y=newY
        
    #calculate the G force on the object
    def applyG(self,other,G):
        #calculate r between the objects
        dx = other.__x - self.__x
        dy = other.__y - self.__y
        r=(dx**2+dy**2)**0.5
        #print(dx)
        #print(dy)
        #print(r)
        if r==0:
            return
        
        #calculate a and apply it as a vector to ax and ay
        a = (G*other.__m)/(r**2)
        self.__ax = self.__ax+a*(dx/r)
        self.__ay = self.__ay+a*(dy/r)

        a = (G*self.__m)/(r**2)
        other.__ax = other.__ax+a*(-dx/r)
        other.__ay = other.__ay+a*(-dy/r)
    
    #function to update body position according to acceleration on body
    def update(self,dt):
        self.__vx=self.__vx+self.__ax*dt
        self.__vy=self.__vy+self.__ay*dt
        self.__x=self.__x+self.__vx*dt
        self.__y=self.__y+self.__vy*dt
        self.__trail.append([self.__x,self.__y])
        
        self.__ax=0
        self.__ay=0