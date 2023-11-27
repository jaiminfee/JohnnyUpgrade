from cmu_graphics import *
import random
import math

#JOHNNY CLASS------------------------------------------------------
class Johnny:
   def __init__(self):
       self.abilities = ['Speed', 'Jump Power', 'Double Jump', 'Time Limit',
                 'Energy', 'Gun Power', 'Gun Ammo', 'Multiplier']
       self.reachedGun = False
       self.levels = [1, 1, 0, 1, 1, 0, 0, 1]
       self.maxLevels = [10, 10, 1, 24, 5, 1, 1, 10]
       self.price = [1, 2, -1, 10, 5, -1, -1, 20]
       self.money = 1
      
      
   def getLevel(self, i):
       return self.levels[i]
  
   def getMaxLevel(self, i):
       return self.maxLevels[i]
  
   def getGunStatus(self):
       return self.reachedGun
  
   def getDoubleJump(self):
       return self.levels[1]==self.maxLevels[1]
  
   def incrementTrait(self, i):
       if self.levels[i]!=self.maxLevels[i] and self.money>= self.price[i]:
           self.levels[i]+=1
           self.money-=self.price[i]
           self.price[i] = (self.price[i] + (2)**self.levels[i])//1
  
   def getSpeedConversion(self):
       if self.levels[0] == 1:
           return 0
       return self.levels[0] + (1.2)**self.levels[0]
  
   def getJumpConversion(self):
       if self.levels[1] == 1:
           return 0
       return self.levels[1] + (1.1)**self.levels[1]
  
   def getTimeConversion(self):
       if self.levels[3]==1:
           return 4
       else:
           return 5 +  math.ceil(1.5*self.levels[3])
  
   def getPrice(self, i):
       if self.price[i]>0:
           return self.price[i]
       else:
           return 'Locked!'
      
   def getMoney(self):
       return self.money
   
   def addMoney(self):
        self.money += 1 * self.levels[7]

   def died(self):
    self.health
  


#Coins class------------------------------------------------------
class coin:
    locations = []
    def __init__(self, x, y):
        self.value = 1
        self.x = x
        self.y = y
        self.radius = 15
        coin.locations.append((x, y))

    
        
        
#Enemies ARRIVING SOON------------------------------------------------------
class enemy:
   def __init__(self):
       self.health = 1


#Shapes Class------------------------------------------------------
class shape:
   bx = []
   tx = []
   ry = []
   ly = []
   shapes = 0
   lengths = []
   heights = []
   def __init__(self, ox, oy, l, h, s):   
       shape.bx.append(midpoint(ox, oy+h, ox+l, oy+h))
       shape.tx.append(midpoint(ox, oy, ox+l, oy))
       shape.ry.append(midpoint(ox+l, oy, ox+l, oy+h))
       shape.ly.append(midpoint(ox, oy, ox, oy+h))
       shape.shapes+=1
       shape.lengths.append(l)
       shape.heights.append(h)

#Obstacle Class ARRIVING SOON--------------------------------------------------
class obstacle:
    bx = []
    tx = []
    ry = []
    ly = []
    obstacles = 0
    lengths = []
    heights = []
    def __init__(self, ox, oy, l, h, s):    
        obstacle.bx.append(midpoint(ox, oy+h, ox+l, oy+h))
        obstacle.tx.append(midpoint(ox, oy, ox+l, oy))
        obstacle.ry.append(midpoint(ox+l, oy, ox+l, oy+h))
        obstacle.ly.append(midpoint(ox, oy, ox, oy+h))
        obstacle.obstacles+=1
        obstacle.lengths.append(l)
        obstacle.heights.append(h)




#Helper math functions------------------------------------------------------


def distance(x1, y1, x2, y2):
   return ((x1-x2)**2 + (y1-y2)**2)**0.5


def midpoint(x1, y1, x2, y2):
   return((x1+x2)/2, (y1+y2)/2)


def almostEqualsV(x, y):
   return abs(x-y)<=15


def almostEqualsH(app, x, y):
   return abs(x-y)<=5+app.player.getLevel(0)




def onAppStart(app):
   #General New Game necessities------------------------------------------------------
   app.newGame = False
   app.start = False
   app.money = 1
   app.timeLeft = 0
   app.won = False
   app.height = 830
   app.width = 1515
   app.traits = ['Speed', 'Jump Power', 'Double Jump', 'Time Limit',
                 'Energy', 'Gun Power', 'Gun Ammo', 'Multiplier']
   app.gravity = True
   app.action = False
  
   #Upgrade buttons------------------------------------------------------
   app.dots = []
   app.player = None
   app.selectedDotIndex = -1


   #Jumping Mechanics------------------------------------------------------
   app.jumping = False
   app.falling = False
   app.stepsPerSecond = 500
   app.count = 0




#Scrolling mechanics------------------------------------------------------
   app.scrollX = 0

   app.canMoveRight = True
   app.canMoveLeft = True
   app.canMoveY = True


#Shapes instances!
   app.bx = ()
   app.tx = ()
   app.ry = ()
   app.ly = ()
  
  #landMass1
   shape(0-app.scrollX, app.height-(app.height/4),
                app.width, app.height/4, app.scrollX)
   shape(app.width+200-app.scrollX, app.height-(app.height/4)-50, 500,
          app.height/4+50, app.scrollX)
   shape(0-app.scrollX, app.height-(app.height/4)-50, 500, 50, app.scrollX)
   
   #landMass2
   shape(1000, app.height-(app.height/4)-75, app.width-1000, 75, app.scrollX)
   
   shape(-100, 100, 100, app.height, app.scrollX)
   
   #landMass 3
   shape(app.width+1000-app.scrollX, app.height-50, app.width,
          50, app.scrollX)
   
   shape(app.width*2+1000-app.scrollX, 0, app.width,
          app.height-100, app.scrollX)

    #stairs
   shape(app.width+1350-app.scrollX, app.height-50-150, 100,
          20, app.scrollX)
   shape(app.width+1700-app.scrollX, app.height-50-300, 325,
          20, app.scrollX)

   


def onKeyHold(app, keys):
   #Moving Character left to right------------------------------------------------------
   if 'right' in keys and 'left' not in keys and app.canMoveRight:
       app.scrollX+= app.player.getSpeedConversion()
   elif 'left' in keys and 'right' not in keys and app.canMoveLeft:
       app.scrollX-= app.player.getSpeedConversion()



#On press Jump------------------------------------------------------
def onKeyPress(app, key):
   if 'up' == key and not app.gravity and app.canMoveY:
       app.count = 0
       app.jumping = True


def onMousePress(app, mouseX, mouseY):
   #To Start a new game------------------------------------------------------
   if not app.newGame and (distance(mouseX, mouseY, app.width/2 - 50, app.height/2+75) <= 200):
       app.newGame = True
       app.player = Johnny()

    #Check if an item is upgraded------------------------------------------------------
   if getDotIndex(app, mouseX, mouseY) !=None:
       app.selectedDotIndex = getDotIndex(app, mouseX, mouseY)
       if app.player.getPrice(app.selectedDotIndex) != 'Locked!':
           app.player.incrementTrait(app.selectedDotIndex)

    #Begin New run------------------------------------------------------
   if distance(mouseX, mouseY, 570, 765) <=25:
       app.start = True
       play(app)




def redrawAll(app):
   if not app.newGame:
       #Drawing Start Screen------------------------------------------------------
       drawRect(0,0, app.width, app.height)
       drawCircle(app.width/2 - 50, app.height/2+75, 200, fill = 'white')
   elif not app.start:
       #Drawing Buy Screen------------------------------------------------------
       drawRect(0,0, app.width, app.height)
       drawRect(100, 100, 1000, 700)
       counter = 0
       for i in range(100, 801, 70):
           drawLine(100, i, 1100, i, fill = 'white')
           if i == 100:
               drawLine(550, i, 550, i+70)
               drawLabel(f'$: {app.player.getMoney()}', 200, 135, fill = 'white', size = 25)
           elif counter<len(app.traits):
               if counter == 2 and not app.player.getDoubleJump():
                   drawCircle(150, i+ (70/2) , 25, fill = 'red')
                   drawLabel(f'{app.traits[counter]}: ${app.player.getPrice(counter)}',
                             350, i + (70/2), fill = 'blue', size = 25, opacity= 25)
                   drawLabel(f'Locked!', 950, i+(70/2), fill = 'white', size = 25, opacity= 25)
               elif counter == 5 and not app.player.getGunStatus():
                   drawCircle(150, i+ (70/2) , 25, fill = 'red')
                   drawLabel(f'{app.traits[counter]}: ${app.player.getPrice(counter)}',
                             350, i + (70/2), fill = 'blue', size = 25, opacity= 25)
                   drawLabel(f'Locked!', 950, i+(70/2), fill = 'white', size = 25, opacity= 25)
               elif counter == 6 and not app.player.getGunStatus():
                   drawCircle(150, i+ (70/2) , 25, fill = 'red')
                   drawLabel(f'{app.traits[counter]}: ${app.player.getPrice(counter)}',
                             350, i + (70/2), fill = 'blue', size = 25, opacity= 25)
                   drawLabel(f'Locked!', 950, i+(70/2), fill = 'white', size = 25, opacity= 25)
               elif app.player.getMoney()< app.player.getPrice(counter):
                   drawCircle(150, i+ (70/2) , 25, fill = 'red')
                   drawLabel(f'{app.traits[counter]}: ${app.player.getPrice(counter)}',
                             350, i + (70/2), fill = 'blue', size = 25, opacity= 25)
                   drawLabel(f'Level: {app.player.getLevel(counter)}/{app.player.getMaxLevel(counter)}',
                              950, i+(70/2), fill = 'white', size = 25, opacity= 25)
               else:
                   drawCircle(150, i+ (70/2) , 25, fill = 'green')
                   drawLabel(f'{app.traits[counter]}: ${app.player.getPrice(counter)}', 350, i + (70/2),
                         fill = 'blue', size = 25)
                   drawLabel(f'Level: {app.player.getLevel(counter)}/{app.player.getMaxLevel(counter)}',
                          950, i+(70/2), fill = 'white', size = 25)
               counter+=1
               app.dots.append((150, i+(70/2)))
           if i == 730:
               drawCircle(570, i+ (70/2) , 25, fill = 'green')
               drawLabel('Play', 640, i + (70/2), fill = 'white', size = 35)
        
       #drawing the playing screen---------------------------------------------
   else:
       #drawing background
       drawRect(0, 0, app.height, app.width, fill = 'cyan', opacity = 25)
       drawRect(830, 0, app.height, app.width, fill = 'cyan', opacity = 25)
      
       #drawing playing screen
       #time/health/money------------------------------------------------------
       drawLabel(f'{math.floor(app.timeLeft)}', app.width/2, 30, fill = 'black', size = 50)
       drawLabel(f'$: {app.player.getMoney()}', 125, 30, fill = 'black', size = 50)
       for i in range(app.health):
            drawCircle(app.width-225+(i*50), 50, 25, fill = 'red')
    
     
      #player------------------------------------------------------
       drawRect(app.cx, app.cy, 150, 200)


       #shapes------------------------------------------------------
       #landMass1
       drawRect(0-app.scrollX, app.height-(app.height/4),
                app.width, app.height/4, fill = 'green')
       drawRect(app.width+200-app.scrollX, app.height-(app.height/4)-50, 500,
          app.height/4+50, fill = 'green')
       drawRect(0-app.scrollX, app.height-(app.height/4)-50, 500, 50, fill = 'green')
       
        #landMass2
       drawRect(1000-app.scrollX, app.height-(app.height/4)-75,
                app.width-1000, 75, fill = 'green')
       
       drawRect(-100-app.scrollX, 100, 100, app.height, fill = 'brown')

       #landMass3
       drawRect(app.width+1000-app.scrollX, app.height-50, app.width,
          50, fill = 'green')
       
       drawRect(app.width*2+1000-app.scrollX, 100, app.width,
          app.height-100, fill = 'brown')
       
       #stairs
       drawRect(app.width+1350-app.scrollX, app.height-50-150, 100,
          20, fill = 'black')
       drawRect(app.width+1700-app.scrollX, app.height-50-300, 325,
          20, fill = 'black')

        #Coins------------------------------------------------------
       for (x, y) in coin.locations:
            drawCircle(x-app.scrollX, y, 15, 
                       fill = 'yellow', border = 'black')
      




#Helper function for upgrade screen: returns index of dot that is pressed--------
def getDotIndex(app, mouseX, mouseY):
   for i in range(len(app.dots)):
       (x, y) = app.dots[i]
       if distance(x, y, mouseX, mouseY)<= 25:
           return i
   return None




#Check if player is able to move------------------------------------------------------


def checkCanMoveDown(app):
   for i in range(shape.shapes):
       if almostEqualsV(app.bx[1], shape.tx[i][1]):
           if distance(app.bx[0], app.bx[1], shape.tx[i][0], shape.tx[i][1]) <= shape.lengths[i]/2+75:
               app.cy = shape.tx[i][1]-200
               return True
   return False
              
          
def checkCanMoveRight(app):
   for i in range(shape.shapes):
       if almostEqualsH(app, app.ry[0], shape.ly[i][0]):
               if shape.heights[i]>200:
                   if distance(app.ry[0], app.ry[1], shape.ly[i][0], shape.ly[i][1]) <= shape.heights[i]/2:
                       return False
               else:
                   if distance(app.ry[0], app.ry[1], shape.ly[i][0], shape.ly[i][1]) <= 100:
                       return False
   return True


def checkCanMoveLeft(app):
   for i in range(shape.shapes):
       if almostEqualsH(app, app.ly[0], shape.ry[i][0]):
               if shape.heights[i]>200:
                   if distance(app.ly[0], app.ly[1], shape.ry[i][0], shape.ry[i][1]) <= shape.heights[i]/2:
                       return False
               else:
                   if distance(app.ly[0], app.ly[1], shape.ry[i][0], shape.ry[i][1]) <= 100:
                       return False
   return True


def updateCharacter(app, ox, oy, l, h):
   app.bx = midpoint(ox, oy+h, ox+l, oy+h)
   app.tx = midpoint(ox, oy, ox+l, oy)
   app.ry = midpoint(ox+l, oy, ox+l, oy+h)
   app.ly = midpoint(ox, oy, ox, oy+h)


def updateMovement(app):
   if not checkCanMoveRight(app):
       app.canMoveRight = False
   else:
       app.canMoveRight = True


   if not checkCanMoveLeft(app):
       app.canMoveLeft = False
   else:
       app.canMoveLeft = True

#Each new trial------------------------------------------------------
def play(app):
        app.timeLeft = app.player.getTimeConversion()
        app.health = app.player.getLevel(4)
        app.scrollX = 0
        app.cx = app.width/2 - 75
        app.cy = (app.height-(app.height//4)) - 200
        #mass 1 coins
        for i in range(0, 99, 33):
            coin(app.cx-100-i, app.cy+100)

        #mass2 coins
            #for i in range(0, 400, 40):
                #coin(1000-app.scrollX+i+69, app.height-(app.height/4)-75-100)
        
        #mass3 coins
            #for i in range(0, 800, 40):
                #coin(app.width+1000+600-app.scrollX+i, app.height-50-100)
                #coin(app.width+1000+600-app.scrollX+i+25, app.height-50-100-50)
           



#Checks throughout run------------------------------------------------------
def onStep(app):
   #if run has started
   if app.start:
       updateCharacter(app, app.cx+app.scrollX, app.cy, 150, 200)
       updateMovement(app)
       #Check if jumping
       if not app.action:
           if checkCanMoveDown(app):
               app.gravity = False
           else:
               app.gravity = True
               updateMovement(app)


       if app.jumping and app.count<100:
           app.action = True
           app.cy-=app.player.getJumpConversion()
           app.count+=5
           if app.count == 100:
               app.jumping = False
               app.action = False
               app.count = 0
       if app.gravity:
           app.cy+=15
           updateMovement(app)
      
      #check if time ran out------------------------------------------------------
       app.timeLeft-=0.0121
       if app.timeLeft<=0 or app.health <1:
            app.start = False

        #check if coins are collected------------------------------------------------------
       for (x, y) in coin.locations:
           if distance(app.cx+75+app.scrollX, app.cy+100, x, y) <= 15+80:
               coin.locations.remove((x, y))
               app.player.addMoney()
        
        #check if dead------------------------------------------------------
       if app.cy > app.height:
            app.health = 0        


def main():
   runApp()


main()



